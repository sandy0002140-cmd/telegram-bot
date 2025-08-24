import os
import telebot
from telebot import types

# === CONFIGURATION via environment ===
TOKEN = os.getenv("8351833418:AAETHk2sXH2ZDSar4oH97tcAne4UhfDbHZc")
ADMIN_ID = int(os.getenv("1038164990"))
CHANNEL_LINK = os.getenv("https://t.me/+GBNJ75WqPHVhYTBl")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🙏 Welcome! इस ALL in One channel को join करने के लिए ₹49 का payment करें।"
    )
    # qr.png ko reliable path se open karo
    try:
        qr_path = os.path.join(os.path.dirname(__file__), "qr.png")
        with open(qr_path, "rb") as f:
            bot.send_photo(
                message.chat.id,
                f,
                caption="यह रहा आपका QR Code। Payment करने के बाद screenshot भेजें।"
            )
    except Exception:
        bot.send_message(message.chat.id, "⚠️ QR image missing. Admin se contact karein.")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    try:
        file_id = message.photo[-1].file_id
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.chat.id}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}")
        )
        caption = f"📸 Screenshot user {message.chat.id} se aaya hai.\n\n👇 Action choose karein:"
        bot.send_photo(ADMIN_ID, file_id, caption=caption, reply_markup=markup)
        bot.send_message(message.chat.id, "📩 Screenshot मिल गया है। Admin verify करने के बाद reply मिलेगा।")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"⚠️ Error screenshot bhejte waqt: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def callback_handler(call):
    user_id = int(call.data.split("_")[1])
    if call.message.chat.id == ADMIN_ID:
        try:
            if call.data.startswith("approve_"):
                bot.send_message(user_id, f"✅ Payment verified!\nयह रहा आपका channel link:\n{CHANNEL_LINK}")
                bot.send_message(ADMIN_ID, f"User {user_id} को access दे दिया गया ✅")
                bot.answer_callback_query(call.id, "User approved!")
            else:
                bot.send_message(user_id, "❌ आपका screenshot reject कर दिया गया है। कृपया सही screenshot भेजें।")
                bot.send_message(ADMIN_ID, f"User {user_id} ka screenshot reject kar diya gaya ❌")
                bot.answer_callback_query(call.id, "User rejected!")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Error: {e}")
    else:
        bot.answer_callback_query(call.id, "आप admin नहीं हो!")

if __name__ == "__main__":
    print("🤖 Bot chal raha hai...")
    bot.polling(none_stop=True, interval=0, timeout=20)
