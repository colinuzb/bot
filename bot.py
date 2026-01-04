import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiException

TOKEN = "8045767418:AAF7XXhXqG9a_uT2uQaEAPiFaRWpTYQltds"
OWNER_ID = 7788334322  # Sizning ID
REQUIRED_CHANNELS = ["@colinuzb", "@ibrohimweb"]  # majburiy kanallar

bot = telebot.TeleBot(TOKEN)

users = {}
buttons = {}
admins = set()  # adminlar ro'yxati

# Owner keyboard
def owner_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("𝐒𝐭𝐚𝐭𝐮𝐬"), KeyboardButton("💥𝐓𝐮𝐠𝐦𝐚 𝐲𝐚𝐫𝐚𝐭𝐢𝐬𝐡💥"), KeyboardButton("🧑𝐀𝐝𝐦𝐢𝐧 𝐪𝐨❜𝐬𝐡𝐢𝐬𝐡🧑"))
    return markup

# User keyboard
def user_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for title in buttons.keys():
        markup.add(KeyboardButton(title))
    return markup

# Foydalanuvchi kanallarga obuna bo'lganini tekshirish
def check_channels(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except ApiException:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    users[user_id] = username

    if user_id == OWNER_ID:
        bot.send_message(message.chat.id, "𝐂𝐨𝐥𝐢𝐧 𝐩𝐚𝐧𝐞𝐥𝐠𝐚 𝐱𝐮𝐬𝐡 𝐤𝐞𝐥𝐢𝐛𝐬𝐢𝐳❗", reply_markup=owner_keyboard())
    else:
        if not check_channels(user_id):
            msg = "𝐁𝐨𝐭𝐝𝐚𝐧 𝐟𝐨𝐲𝐝𝐚𝐥𝐚𝐧𝐢𝐬𝐡 𝐮𝐜𝐡𝐮𝐧 𝐪𝐮𝐲𝐢𝐝𝐚𝐠𝐢 𝐤𝐚𝐧𝐚𝐥𝐥𝐚𝐫𝐠𝐚 𝐨𝐛𝐮𝐧𝐚 𝐛𝐨‘𝐥𝐢𝐧𝐠:\n"
            msg += "\n".join(REQUIRED_CHANNELS)
            bot.send_message(message.chat.id, msg)
            return
        if buttons:
            bot.send_message(message.chat.id, "𝐐𝐮𝐲𝐢𝐝𝐚𝐠𝐢 𝐭𝐮𝐠𝐦𝐚𝐥𝐚𝐫 𝐦𝐚𝐯𝐣𝐮𝐝:", reply_markup=user_keyboard())
        else:
            bot.send_message(message.chat.id, "𝐇𝐨𝐳𝐢𝐫𝐜𝐡𝐚 𝐭𝐮𝐠𝐦𝐚 𝐦𝐚𝐯𝐣𝐮𝐝 𝐞𝐦𝐚𝐬.")

# Matnli tugmalarni boshqarish
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    # Owner
    if user_id == OWNER_ID:
        if text == "𝐒𝐭𝐚𝐭𝐮𝐬":
            if users:
                user_list = "\n".join([f"{uid}: {uname}" for uid, uname in users.items()])
                bot.send_message(message.chat.id, f"𝐁𝐨𝐭𝐠𝐚 𝐬𝐭𝐚𝐫𝐭 𝐛𝐨𝐬𝐠𝐚𝐧 𝐟𝐨𝐲𝐝𝐚𝐥𝐚𝐧𝐮𝐯𝐜𝐡𝐢𝐥𝐚𝐫 ({len(users)}):\n{user_list}")
            else:
                bot.send_message(message.chat.id, "𝐇𝐚𝐥𝐢 𝐡𝐞𝐜𝐡 𝐤𝐢𝐦 𝐬𝐭𝐚𝐫𝐭 𝐛𝐨𝐬𝐦𝐚𝐠𝐚𝐧.")
        elif text == "💥𝐓𝐮𝐠𝐦𝐚 𝐲𝐚𝐫𝐚𝐭𝐢𝐬𝐡💥":
            msg = bot.send_message(message.chat.id, "𝐓𝐮𝐠𝐦𝐚 𝐮𝐜𝐡𝐮𝐧 𝐧𝐨𝐦 𝐲𝐨𝐳𝐢𝐧𝐠:")
            bot.register_next_step_handler(msg, get_title)
        elif text == "🧑𝐀𝐝𝐦𝐢𝐧 𝐪𝐨❜𝐬𝐡𝐢𝐬𝐡🧑":
            msg = bot.send_message(message.chat.id, "𝐀𝐝𝐦𝐢𝐧 𝐪𝐢𝐥𝐦𝐨𝐪𝐜𝐡𝐢 𝐛𝐨❜𝐥𝐠𝐚𝐧 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐧𝐢 𝐤𝐢𝐫𝐢𝐭𝐢𝐧𝐠:")
            bot.register_next_step_handler(msg, add_admin)
    else:
        # Oddiy foydalanuvchi tugmani bosganda linkni yuborish
        if text in buttons:
            link = buttons[text]
            bot.send_message(message.chat.id, f"🔥𝐁𝐨𝐭𝐝𝐚𝐧 𝐟𝐨𝐲𝐝𝐚𝐥𝐚𝐧𝐠𝐚𝐧𝐢𝐧𝐠𝐢𝐳 𝐮𝐜𝐡𝐮𝐧 𝐤𝐚𝐭𝐭𝐚𝐤𝐨𝐧 𝐫𝐚𝐡𝐦𝐚𝐭😃: {link}")

# Owner title so'rash
def get_title(message):
    title = message.text
    msg = bot.send_message(message.chat.id, f"'{title}' 𝐓𝐮𝐠𝐦𝐚 𝐮𝐜𝐡𝐮𝐧 𝐬𝐢𝐥𝐤𝐚 𝐲𝐮𝐛𝐨𝐫𝐢𝐧𝐠:")
    bot.register_next_step_handler(msg, get_link, title)

# Owner link so'rash
def get_link(message, title):
    link = message.text
    buttons[title] = link
    bot.send_message(message.chat.id, f"𝐓𝐮𝐠𝐦𝐚 '{title}' 𝐲𝐚𝐫𝐚𝐭𝐢𝐥𝐝𝐢!")

# Owner admin qo'shish
def add_admin(message):
    try:
        admin_id = int(message.text)
        admins.add(admin_id)
        bot.send_message(message.chat.id, f"{admin_id} 𝐚𝐝𝐦𝐢𝐧 𝐬𝐢𝐟𝐚𝐭𝐢𝐝𝐚 𝐪𝐨❜𝐬𝐡𝐢𝐥𝐝𝐢❗")
    except ValueError:
        bot.send_message(message.chat.id, "𝐈𝐥𝐭𝐢𝐦𝐨𝐬, 𝐭𝐨❜𝐠❜𝐫𝐢 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐤𝐢𝐫𝐢𝐭𝐢𝐧𝐠.")

bot.infinity_polling()
