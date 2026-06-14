import os
from threading import Thread
from flask import Flask
import telebot

# আপনার দেওয়া ডিটেইলস
API_TOKEN = '8632186250:AAFXjRo6YltjHBy2wSdqcRcxC8lzw6dNFt0'
ADMIN_ID = '@romankhan10100'  # ইউজারনেম হ্যান্ডেল করার জন্য

bot = telebot.TeleBot(API_TOKEN)
app = Flask()

# Render-এর জন্য ডামি ওয়েব সার্ভার (Ping রাখার জন্য)
@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_web_server():
    # Render অটোমেটিক PORT অ্যাসাইন করে, না থাকলে 8080 ব্যবহার করবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# বটের কমান্ড এবং মেসেজ হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        f"আসসালামু আলাইকুম, **{message.from_user.first_name}**!\n\n"
        f"আমি **pythonbotpy_bot**। আপনাকে সাহায্য করতে প্রস্তুত।\n"
        f"যেকোনো প্রয়োজনে ওনার {ADMIN_ID} এর সাথে যোগাযোগ করুন।"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # ইউজার কোনো মেসেজ দিলে বট রিপ্লাই দেবে
    bot.reply_to(message, f"আপনি বললেন: {message.text}")

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ওয়েব সার্ভার চালু করা হচ্ছে
    server_thread = Thread(target=run_web_server)
    server_thread.start()
    
    print("Bot is polling...")
    bot.infinity_polling()
    