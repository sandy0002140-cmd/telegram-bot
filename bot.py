import telebot
from telebot import types

# === CONFIGURATION ===
TOKEN = "8351833418:AAETHk2sXH2ZDSar4oH97tcAne4UhfDbHZc"   # BotFather se mila token
ADMIN_ID = 1038164990      # Apna numeric Telegram User ID
CHANNEL_LINK = "https://t.me/+GBNJ75WqPHVhYTBl"  # Channel link

bot = telebot.TeleBot(TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🙏 Welcome! इस ALL in One channel को join करने के लिए ₹49 का payment करें।"
    )
    bot.send_photo(
        message.chat.id,
        open("qr.png", "rb"),
        caption="यह रहा आपका QR Code। Payment करने के बाद screenshot भेजें।"
    )

# जब user screenshot भेजे
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    try:
        # User ne jo photo bheja uska file_id nikal lo
        file_id = message.photo[-1].file_id  

        # Admin ke liye approve/reject buttons
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.chat.id}")
        btn2 = types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}")
        markup.add(btn1, btn2)

        caption = f"📸 Screenshot user {message.chat.id} se aaya hai.\n\n👇 Action choose karein:"
        # Yehi same photo admin ko bhejna
        bot.send_photo(ADMIN_ID, file_id, caption=caption, reply_markup=markup)

        # User ko notify karo
        bot.send_message(
            message.chat.id,
            "📩 Screenshot मिल गया है। Admin verify करने के बाद आपको reply मिलेगा।"
        )
    except Exception as e:
        bot.send_message(ADMIN_ID, f"⚠️ Error screenshot bhejte waqt: {e}")

# Callback handler (Approve/Reject button ke liye)
@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def callback_handler(call):
    user_id = int(call.data.split("_")[1])

    if call.message.chat.id == ADMIN_ID:  # Sirf admin buttons use kar sakta hai
        if call.data.startswith("approve_"):
            try:
                bot.send_message(user_id, f"✅ Payment verified!\nयह रहा आपका channel link:\n{CHANNEL_LINK}")
                bot.send_message(ADMIN_ID, f"User {user_id} को access दे दिया गया ✅")
                bot.answer_callback_query(call.id, "User approved!")
            except Exception as e:
                bot.send_message(ADMIN_ID, f"❌ Error: {e}")

        elif call.data.startswith("reject_"):
            try:
                bot.send_message(user_id, "❌ आपका screenshot reject कर दिया गया है। कृपया सही screenshot भेजें।")
                bot.send_message(ADMIN_ID, f"User {user_id} ka screenshot reject kar diya gaya ❌")
                bot.answer_callback_query(call.id, "User rejected!")
            except Exception as e:
                bot.send_message(ADMIN_ID, f"❌ Error: {e}")
    else:
        bot.answer_callback_query(call.id, "आप admin नहीं हो!")

# === Bot start ===
print("🤖 Bot chal raha hai...")
bot.polling(none_stop=True, interval=0, timeout=20)
