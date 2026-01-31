import asyncio
import logging
import os
from io import BytesIO

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, 
    BufferedInputFile, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    CallbackQuery
)
from PIL import Image

# ==========================================
# ⚙️ SOZLAMALAR
# ==========================================
# 👇 TOKENNI SHU YERGA YOZING
BOT_TOKEN = "8045767418:AAF7XXhXqG9a_uT2uQaEAPiFaRWpTYQltds"

# Skinlar turadigan papka nomi
SKINS_FOLDER = "skins"

# Loglarni yoqish (xatolarni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# ==========================================
# 🎨 RASM ISHLASH (SKIN RENDERER)
# ==========================================
class SkinRenderer:
    @staticmethod
    def get_head(skin_path: str):
        """Skin faylidan faqat Bosh qismini qirqib oladi"""
        try:
            img = Image.open(skin_path).convert("RGBA")
            # Minecraft skinida Bosh qismi: (8, 8) dan (16, 16) gacha
            head = img.crop((8, 8, 16, 16)) 
            # 8x8 rasmni 256x256 ga kattalashtiramiz
            head = head.resize((256, 256), resample=Image.Resampling.NEAREST)
            return head
        except Exception as e:
            print(f"Rasm xatosi: {e}")
            return None

    @staticmethod
    def get_body(skin_path: str):
        """Skin faylidan Tana (Body) yasaydi"""
        try:
            img = Image.open(skin_path).convert("RGBA")
            
            # Yangi bo'sh kanvas (160x320)
            canvas = Image.new("RGBA", (160, 320), (0, 0, 0, 0))
            
            # Qismlarni qirqib olish va kattalashtirish (x10)
            head = img.crop((8, 8, 16, 16)).resize((80, 80), Image.Resampling.NEAREST)
            body = img.crop((20, 20, 28, 32)).resize((80, 120), Image.Resampling.NEAREST)
            arm = img.crop((44, 20, 48, 32)).resize((40, 120), Image.Resampling.NEAREST)
            leg = img.crop((4, 20, 8, 32)).resize((40, 120), Image.Resampling.NEAREST)

            # Yopishtirish (Koordinatalar bo'yicha)
            canvas.paste(head, (40, 0))    # Bosh
            canvas.paste(body, (40, 80))   # Tana
            canvas.paste(arm, (0, 80))     # O'ng qo'l
            canvas.paste(arm, (120, 80))   # Chap qo'l
            canvas.paste(leg, (40, 200))   # O'ng oyoq
            canvas.paste(leg, (80, 200))   # Chap oyoq

            return canvas
        except Exception as e:
            print(f"Rasm xatosi: {e}")
            return None

# ==========================================
# ⌨️ TUGMALAR (KEYBOARDS)
# ==========================================
def get_skins_keyboard():
    """Papkadagi fayllarga qarab tugma yasaydi"""
    if not os.path.exists(SKINS_FOLDER):
        os.makedirs(SKINS_FOLDER)
    
    # Faqat .png fayllarni o'qiymiz
    files = [f for f in os.listdir(SKINS_FOLDER) if f.endswith(".png")]
    files.sort()
    
    keyboard = []
    row = []
    for file in files:
        name = file.replace(".png", "") # .png ni olib tashlaymiz
        btn = InlineKeyboardButton(text=f"👤 {name}", callback_data=f"skin:{file}")
        row.append(btn)
        
        # Har qatorda 2 tadan tugma
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_view_keyboard(filename):
    """Ko'rinishni tanlash tugmasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Bosh (Head)", callback_data=f"render:head:{filename}"),
            InlineKeyboardButton(text="🕴 Tana (Body)", callback_data=f"render:body:{filename}")
        ],
        [
            InlineKeyboardButton(text="🔙 Bosh Menyu", callback_data="back_home")
        ]
    ])

# ==========================================
# 🤖 BOT MANTIQI (HANDLERS)
# ==========================================
router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message):
    # Papka bo'shligini tekshiramiz
    files = [f for f in os.listdir(SKINS_FOLDER) if f.endswith(".png")]
    
    if not files:
        await message.answer(
            f"📂 **{SKINS_FOLDER}** papkasi bo'sh!\n\n"
            "Iltimos, bot ishlashi uchun u yerga **.png** formatdagi skin tashlang."
        )
        return

    await message.answer(
        "👋 **Assalomu alaykum!**\n\n"
        "Qaysi skinni tanlamoqchisiz? Marhamat:",
        reply_markup=get_skins_keyboard()
    )

# ✅ TUZATILGAN "ORQAGA" TUGMASI
@router.callback_query(F.data == "back_home")
async def go_back(callback: CallbackQuery):
    # Eski rasm xabarini o'chiramiz
    try:
        await callback.message.delete()
    except:
        pass 
    
    # Yangi menyu yuboramiz
    await callback.message.answer(
        "Asosiy menyu. Skinni tanlang:",
        reply_markup=get_skins_keyboard()
    )

@router.callback_query(F.data.startswith("skin:"))
async def select_skin(callback: CallbackQuery):
    filename = callback.data.split(":")[1]
    name = filename.replace(".png", "")
    
    # Bu yerda edit_text ishlaydi, chunki oldingi xabar matn edi
    try:
        await callback.message.edit_text(
            f"✅ **{name}** tanlandi.\nQanday ko'rinishda xohlaysiz?",
            reply_markup=get_view_keyboard(filename)
        )
    except:
        # Agar rasm bo'lsa o'chirib yangitdan yozamiz
        await callback.message.delete()
        await callback.message.answer(
            f"✅ **{name}** tanlandi.\nQanday ko'rinishda xohlaysiz?",
            reply_markup=get_view_keyboard(filename)
        )

@router.callback_query(F.data.startswith("render:"))
async def render_skin(callback: CallbackQuery):
    _, type_, filename = callback.data.split(":")
    path = os.path.join(SKINS_FOLDER, filename)
    
    if not os.path.exists(path):
        await callback.answer("⚠️ Fayl topilmadi!", show_alert=True)
        return

    await callback.answer("Tayyorlanmoqda...")
    
    # Rasmni yasash
    final_img = None
    if type_ == "head":
        final_img = SkinRenderer.get_head(path)
        caption = f"👤 **{filename.replace('.png', '')}**"
    elif type_ == "body":
        final_img = SkinRenderer.get_body(path)
        caption = f"🕴 **{filename.replace('.png', '')}**"

    if final_img:
        # Rasmni xotiraga olish
        bio = BytesIO()
        final_img.save(bio, 'PNG')
        bio.seek(0)
        
        file = BufferedInputFile(bio.read(), filename=filename)
        
        # Eski xabarni o'chirib, rasm yuboramiz
        await callback.message.delete()
        await callback.message.answer_photo(
            file, 
            caption=caption,
            reply_markup=get_view_keyboard(filename)
        )
    else:
        await callback.message.answer("⚠️ Rasmni yasashda xatolik bo'ldi.")

# ==========================================
# 🚀 ISHGA TUSHIRISH
# ==========================================
async def main():
    if "SIZNING" in BOT_TOKEN:
        print("❌ XATO: Tokenni kod ichiga yozing!")
        return

    if not os.path.exists(SKINS_FOLDER):
        os.makedirs(SKINS_FOLDER)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Bot ishga tushdi! Telegramga kiring.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtadi.")