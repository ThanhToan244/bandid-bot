import logging
import random
import time
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "8928629119:AAEsNQyk81o5zSmykc5RO8jRJCBZ0zu7KOI"
FIREBASE_URL = "https://bandidkey-default-rtdb.firebaseio.com/"
ADMIN_USER_ID = 7539743405

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = (
        "🤖 **BAND ID BOT (CLOUD SERVER)**\n\n"
        "Danh sách lệnh:\n"
        "• /getkey - Lấy link vượt nhận key\n"
        "• /key - Hướng dẫn nhập key\n"
        "• /tk - Kiểm tra tài khoản\n"
        "• /open - Kiểm tra trạng thái mở\n"
        "• /off - Kiểm tra trạng thái bảo trì\n"
    )
    if user_id == ADMIN_USER_ID:
        text += "• /taokey - [QTV] Tạo key nhanh\n"
    update.message.reply_text(text, parse_mode="Markdown")

def getkey(update: Update, context: CallbackContext):
    random_code = f"KEY-{random.randint(100000, 999999)}"
    session_id = f"S_{int(time.time() * 1000)}"
    payload = {"code": random_code, "type": "day", "createdAt": int(time.time() * 1000)}
    requests.put(f"{FIREBASE_URL}keys/{session_id}.json", json=payload)
    
    link4m_url = f"https://link4m.co/st?api=667da5e0512ac00cba52fb6f&url=https://ThanhToan244.github.io/getkey/?session={session_id}"
    update.message.reply_text(f"🎁 **LINK VƯỢT NHẬN KEY:**\n{link4m_url}", parse_mode="Markdown")

def key_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("🔑 **Hướng dẫn:** Copy mã key sau khi vượt link dán vào app Band ID để kích hoạt!", parse_mode="Markdown")

def tk(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    balance = 100000000000000 if user_id == ADMIN_USER_ID else 0
    update.message.reply_text(f"👤 **Tài khoản:** {user_name}\n• ID: `{user_id}`\n• Số dư: {balance:,} VNĐ", parse_mode="Markdown")

def open_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("🟢 **Trạng thái:** Hệ thống Band ID đang hoạt động bình thường!", parse_mode="Markdown")

def off_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("🔴 **Trạng thái:** Hệ thống đang tạm ngưng hoặc bảo trì.", parse_mode="Markdown")

def taokey(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    random_code = f"KEY-{random.randint(1000000, 9999999)}"
    session_id = f"ADMIN_GEN_{int(time.time() * 1000)}"
    requests.put(f"{FIREBASE_URL}keys/{session_id}.json", json={"code": random_code, "type": "day"})
    update.message.reply_text(f"🛠️ **Tạo Key QTV thành công:** `{random_code}`", parse_mode="Markdown")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getkey", getkey))
    dp.add_handler(CommandHandler("key", key_cmd))
    dp.add_handler(CommandHandler("tk", tk))
    dp.add_handler(CommandHandler("open", open_cmd))
    dp.add_handler(CommandHandler("off", off_cmd))
    dp.add_handler(CommandHandler("taokey", taokey))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
