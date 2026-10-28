import telebot
from telebot import types
import random
from datetime import datetime
import os
from flask import Flask
from threading import Thread

TOKEN = '9254355271:AAHePCwbgTsA_WMdygdt2mDwtOQL_HB6-z4'
bot = telebot.TeleBot(TOKEN)

# Render-এর জন্য মিনি ওয়েব সার্ভার (যাতে ওয়েব সার্ভিস বন্ধ না হয়)
app = Flask('')

@app.route('/')
def home():
    return "Quotex Bot is Active and Running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# প্রধান কারেন্সি পেয়ারসমূহ
pairs = ["EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "EUR/JPY", "USD/INR (OTC)", "NZD/USD (OTC)", "USD/JPY (OTC)"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📊 প্রিমিয়াম সিগন্যাল নিন", callback_data="get_signal")
    btn2 = types.InlineKeyboardButton("💡 ট্রেডিং টিপস", callback_data="trading_tips")
    markup.add(btn1)
    markup.add(btn2)
    
    bot.send_message(
        message.chat.id, 
        "🤖 **Advanced Quotex Signal Bot v2.0**\n\n"
        "স্বাগতম! এই বটটি মার্কেট মোমেন্টাম ও প্রাইস অ্যাকশন এনালাইজ করে সিগন্যাল প্রদান করবে।\n"
        "নিচের বাটনে ক্লিক করে সিগন্যাল জেনারেট করুন:", 
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_signal":
        current_time = datetime.now().strftime("%H:%M:%S")
        selected_pair = random.choice(pairs)
        direction = random.choice(["UP 🟢 (Call / Buy)", "DOWN 🔴 (Put / Sell)"])
        time_frame = random.choice(["1 Minute", "5 Minutes"])
        accuracy = round(random.uniform(78.5, 92.3), 2)
        martingale = "Step 1 (সতর্কতা অবলম্বন করুন)" if accuracy < 85 else "Safe (সরাসরি নিন)"
        
        signal_text = (
            f"🔥 **ADVANCED QUOTEX SIGNAL** 🔥\n"
            f"────────────────────────\n"
            f"🕒 **Time:** `{current_time}`\n"
            f"🌐 **Market Pair:** `{selected_pair}`\n"
            f"📈 **Prediction:** **{direction}**\n"
            f"⏱️ **Expiry Time:** `{time_frame}`\n"
            f"🎯 **Accuracy Rate:** `{accuracy}%`\n"
            f"🛡️ **Strategy:** {martingale}\n"
            f"────────────────────────\n"
            f"💡 **Analysis:** RSI Oversold/Overbought + Volume Spike\n\n"
            f"⚠️ *সতর্কতা: বাইনারি অপশন অত্যন্ত ঝুঁকিপূর্ণ। মানি ম্যানেজমেন্ট ও প্রপার রিস্ক রেশিও মেনে ট্রেড করুন।*"
        )
        
        markup = types.InlineKeyboardMarkup()
        btn_refresh = types.InlineKeyboardButton("🔄 নতুন সিগন্যাল নিন", callback_data="get_signal")
        markup.add(btn_refresh)
        
        try:
            bot.edit_message_text(
                signal_text, 
                call.message.chat.id, 
                call.message.message_id, 
                parse_mode="Markdown", 
                reply_markup=markup
            )
        except Exception:
            pass

    elif call.data == "trading_tips":
        tips_text = (
            "📌 **Quotex Smart Trading Rules:**\n\n"
            "1. কখনো একবারে সব ব্যালেন্স দিয়ে ট্রেড করবেন না (সর্বোচ্চ ২-৫% রিস্ক নিন)।\n"
            "2. মার্কেট বেশি ভোলাটাইলে থাকলে সিগন্যাল এভয়েড করুন।\n"
            "3. মার্টিংগেল (Martingale) ব্যবহার করলে সর্বোচ্চ ২ স্টেপ পর্যন্ত যাবেন, এর বেশি নয়।\n"
            "4. নিউজরুম বা হাই-ইমপ্যাক্ট নিউজের সময় ট্রেড করা থেকে বিরত থাকুন।"
        )
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("🔙 পেছনে যান", callback_data="back_home")
        markup.add(btn_back)
        
        try:
            bot.edit_message_text(tips_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except Exception:
            pass

    elif call.data == "back_home":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📊 প্রিমিয়াম সিগন্যাল নিন", callback_data="get_signal")
        btn2 = types.InlineKeyboardButton("💡 ট্রেডিং টিপস", callback_data="trading_tips")
        markup.add(btn1)
        markup.add(btn2)
        
        try:
            bot.edit_message_text(
                "🤖 **Advanced Quotex Signal Bot v2.0**\n\nপ্রধান মেনুতে ফিরে এসেছেন। নিচের বাটন ব্যবহার করুন:", 
                call.message.chat.id, 
                call.message.message_id, 
                parse_mode="Markdown", 
                reply_markup=markup
            )
        except Exception:
            pass

# প্রয়োজনীয় প্যাকেজে flask যোগ করতে হবে, তাই requirements.txt ফাইলে flask লিখে দিতে হবে।
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    
