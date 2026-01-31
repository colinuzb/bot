
# 8045767418:AAF7XXhXqG9a_uT2uQaEAPiFaRWpTYQltds
# 7788334322 

import asyncio
import logging
import sqlite3
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# --- KONFIGURATSIYA ---
API_TOKEN = '8045767418:AAF7XXhXqG9a_uT2uQaEAPiFaRWpTYQltds'
ADMIN_ID = 7788334322  # O'zingizning ID
CHANNELS = ["@colinuzb", "@colincode", "@ibrohimweb"] 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- BAZA ---
db = sqlite3.connect("bot_users.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
db.commit()

# --- MA'LUMOTLAR BAZASI (DATA) ---
# Bu yerda har bir tugma uchun ma'lumotlarni yozib chiqamiz.
# Title, Description va Linkni shu yerdan o'zgartirasiz.
CONTENT_DATA = {
    # O'yinlar
    "Minecraft": {"title": "Minecraft 1.19.8v", "desc": "Minecraft 2025 yili colin tomonidan vzlom qilingan versiya.", "link": "https://t.me/fayl_manzili"},
    "Pubg": {"title": "PUBG Mobile", "desc": "Eng so'nggi versiya, 90 FPS ochilgan.", "link": "https://play.google.com"},
    "Gta V": {"title": "GTA V Mobile", "desc": "Grafikasi kuchaytirilgan norasmiy port.", "link": "https://example.com"},
    "Call Of Duty": {"title": "Call of Duty Mobile", "desc": "Jangovar rejim va yangi xaritalar.", "link": "https://example.com"},
    "Zombie Catshers": {"title": "Zombie Catchers", "desc": "Cheksiz pullar bilan mod qilingan.", "link": "https://example.com"},
    "Farm Ville 2": {"title": "FarmVille 2", "desc": "Fermer xo'jaligi simulyatori.", "link": "https://example.com"},
    "Extreme Car": {"title": "Extreme Car Driving", "desc": "Barcha mashinalar ochilgan.", "link": "https://example.com"},
    "Dr,Driving": {"title": "Dr. Driving", "desc": "Afsonaviy mashina haydash o'yini.", "link": "https://example.com"},
    
    # Ilovalar
    "Telegram": {"title": "Telegram Premium", "desc": "Premium funksiyalar (norasmiy).", "link": "https://example.com"},
    "YouTube": {"title": "YouTube Vanced", "desc": "Reklamasiz YouTube ko'rish.", "link": "https://example.com"},
    "Node Video": {"title": "Node Video Pro", "desc": "Professional video montaj dasturi.", "link": "https://example.com"},
    "Cap Cut": {"title": "CapCut Pro", "desc": "Barcha effektlar ochiq.", "link": "https://example.com"},
    "Alight Motion": {"title": "Alight Motion XML", "desc": "Suv belgisisiz (No Watermark).", "link": "https://example.com"},
    "Zarchiver": {"title": "ZArchiver Pro", "desc": "Fayllarni arxivlash uchun eng zo'r dastur.", "link": "https://example.com"},

    # Dasturlar
    "ChatGpt": {"title": "ChatGPT AI", "desc": "Sun'iy intellekt yordamchisi.", "link": "https://openai.com"},
    "KreaAi": {"title": "Krea AI", "desc": "Rasmlarni generatsiya qilish.", "link": "https://krea.ai"},
    "Design": {"title": "Design Tools", "desc": "Dizaynerlar uchun kerakli to'plam.", "link": "https://example.com"},
    "Upscaler": {"title": "Image Upscaler", "desc": "Rasm sifatini oshiruvchi dastur.", "link": "https://example.com"},
    "Enhancer": {"title": "Photo Enhancer", "desc": "Eski rasmlarni tiklash.", "link": "https://example.com"},

    # Packlar
    "ColinShop": {"title": "Colin Shop Pack", "desc": "Internet magazin uchun tayyor kodlar.", "link": "https://example.com"},
    "Responsive": {"title": "Responsive UI", "desc": "Moslashuvchan dizayn elementlari.", "link": "https://example.com"},
    "Navbar": {"title": "Navbar Pack", "desc": "Saytlar uchun menyu turlari.", "link": "https://example.com"},
    "Animated": {"title": "Animated Pack", "desc": "CSS va JS animatsiyalar.", "link": "https://example.com"},
    "Host": {"title": "Hosting Script", "desc": "Hosting sayti uchun shablon.", "link": "https://example.com"},
    "Portfolio": {"title": "Portfolio Web", "desc": "Shaxsiy portfolio sayt shabloni.", "link": "https://example.com"},
}

# --- TUGMALAR MENU ---
def main_menu(user_id):
    kb = [
        [KeyboardButton(text="O'yinlar"), KeyboardButton(text="Ilovalar")],
        [KeyboardButton(text="Dasturlar"), KeyboardButton(text="Packlar")],
        [KeyboardButton(text="Fayllar")]
    ]
    if user_id == ADMIN_ID:
        kb.append([KeyboardButton(text="⚙️ Sozlama"), KeyboardButton(text="📊 Status")]) # Reklama olib tashlandi
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def sub_channels_kb():
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Obuna bo'lish: {ch}", url=f"https://t.me/{ch[1:]}")] for ch in CHANNELS
    ])
    builder.inline_keyboard.append([InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="check_subs")])
    return builder

# Orqaga tugmasi
back_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Orqaga")]], resize_keyboard=True)

# --- OBUNA TEKSHIRISH ---
async def is_subscribed(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# --- HANDLERLAR ---

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.from_user.id,))
    db.commit()
    if await is_subscribed(message.from_user.id):
        await message.answer("Bosh menyu:", reply_markup=main_menu(message.from_user.id))
    else:
        await message.answer("Botdan foydalanish uchun kanallarga a'zo bo'ling:", reply_markup=sub_channels_kb())

@dp.callback_query(F.data == "check_subs")
async def check_callback(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.delete()
        await call.message.answer("Bosh menyu:", reply_markup=main_menu(call.from_user.id))
    else:
        await call.answer("To'liq obuna bo'lmadingiz!", show_alert=True)

@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu(message.from_user.id))

# --- MENYULAR ---

@dp.message(F.text == "O'yinlar")
async def games_menu(message: types.Message):
    if not await is_subscribed(message.from_user.id): return
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Minecraft"), KeyboardButton(text="Pubg")],
        [KeyboardButton(text="Gta V"), KeyboardButton(text="Call Of Duty")],
        [KeyboardButton(text="Zombie Catshers"), KeyboardButton(text="Farm Ville 2")],
        [KeyboardButton(text="Extreme Car"), KeyboardButton(text="Dr,Driving")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)
    await message.answer("O'yinlar bo'limi:", reply_markup=kb)

@dp.message(F.text == "Ilovalar")
async def apps_menu(message: types.Message):
    if not await is_subscribed(message.from_user.id): return
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Telegram"), KeyboardButton(text="YouTube")],
        [KeyboardButton(text="Node Video"), KeyboardButton(text="Cap Cut")],
        [KeyboardButton(text="Alight Motion"), KeyboardButton(text="Zarchiver")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)
    await message.answer("Ilovalar bo'limi:", reply_markup=kb)

@dp.message(F.text == "Dasturlar")
async def soft_menu(message: types.Message):
    if not await is_subscribed(message.from_user.id): return
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ChatGpt"), KeyboardButton(text="KreaAi")],
        [KeyboardButton(text="Design"), KeyboardButton(text="Upscaler")],
        [KeyboardButton(text="Enhancer"), KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)
    await message.answer("Dasturlar bo'limi:", reply_markup=kb)

@dp.message(F.text == "Packlar")
async def packs_menu(message: types.Message):
    if not await is_subscribed(message.from_user.id): return
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ColinShop"), KeyboardButton(text="Responsive")],
        [KeyboardButton(text="Navbar"), KeyboardButton(text="Animated")],
        [KeyboardButton(text="Host"), KeyboardButton(text="Portfolio")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)
    await message.answer("Packlar bo'limi:", reply_markup=kb)

# --- UNIVERSAL CONTENT HANDLER ---
# Bu funksiya CONTENT_DATA ichidagi istalgan tugma bosilganda ishlaydi
@dp.message(lambda message: message.text in CONTENT_DATA)
async def send_content(message: types.Message):
    if not await is_subscribed(message.from_user.id): return
    
    data = CONTENT_DATA[message.text]
    
    # Rasm nomini yasash (Kichik harf, probel va vergullarni olib tashlash)
    # Misol: "Dr,Driving" -> "drdriving.png"
    clean_name = message.text.lower().replace(" ", "").replace(",", "")
    photo_path = f"img/{clean_name}.png"
    
    caption_text = (
        f"<b>{data['title']}</b>\n\n"
        f"{data['desc']}\n\n"
        f"🤖 @{ (await bot.get_me()).username}"
    )
    
    download_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Yuklab Olish", url=data['link'])]
    ])

    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=caption_text, reply_markup=download_btn, parse_mode="HTML")
    else:
        # Agar rasm topilmasa, shunchaki text boradi (Error bermasligi uchun)
        await message.answer(f"⚠️ Rasm topilmadi: {photo_path}\n\n" + caption_text, reply_markup=download_btn, parse_mode="HTML")

# --- ADMIN STATUS ---
@dp.message(F.text == "📊 Status", F.from_user.id == ADMIN_ID)
async def status_cmd(message: types.Message):
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    await message.answer(f"📊 Botdagi jami foydalanuvchilar: {count} ta")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())