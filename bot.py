import random
import time
import requests
from flask import Flask, request

TOKEN = "8928629119:AAEsNQyk81o5zSmykc5RO8jRJCBZ0zu7KOI"
FIREBASE_URL = "https://bandidkey-default-rtdb.firebaseio.com/"
ADMIN_USER_ID = 7539743405
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        user_name = message["from"].get("first_name", "Bạn")
        text = message.get("text", "").strip()

        if text == "/start":
            reply = (
                "🤖 **BAND ID BOT (CLOUD SERVER)**\n\n"
                "Danh sách lệnh:\n"
                "• /getkey - Lấy link vượt nhận key\n"
                "• /key - Hướng dẫn nhập key\n"
                "• /tk - Kiểm tra tài khoản\n"
                "• /open - Kiểm tra trạng thái mở\n"
                "• /off - Kiểm tra trạng thái bảo trì\n"
            )
            if user_id == ADMIN_USER_ID:
                reply += "• /taokey - [QTV] Tạo key nhanh\n"
            send_message(chat_id, reply)

        elif text == "/getkey":
            random_code = f"KEY-{random.randint(100000, 999999)}"
            session_id = f"S_{int(time.time() * 1000)}"
            payload = {"code": random_code, "type": "day", "createdAt": int(time.time() * 1000)}
            requests.put(f"{FIREBASE_URL}keys/{session_id}.json", json=payload)
            link4m_url = f"https://link4m.co/st?api=667da5e0512ac00cba52fb6f&url=https://ThanhToan244.github.io/getkey/?session={session_id}"
            send_message(chat_id, f"🎁 **LINK VƯỢT NHẬN KEY:**\n{link4m_url}")

        elif text == "/key":
            send_message(chat_id, "🔑 **Hướng dẫn:** Copy mã key sau khi vượt link dán vào app Band ID để kích hoạt!")

        elif text == "/tk":
            balance = 100000000000000 if user_id == ADMIN_USER_ID else 0
            send_message(chat_id, f"👤 **Tài khoản:** {user_name}\n• ID: `{user_id}`\n• Số dư: {balance:,} VNĐ")

        elif text == "/open":
            send_message(chat_id, "🟢 **Trạng thái:** Hệ thống Band ID đang hoạt động bình thường!")

        elif text == "/off":
            send_message(chat_id, "🔴 **Trạng thái:** Hệ thống đang tạm ngưng hoặc bảo trì.")

        elif text == "/taokey" and user_id == ADMIN_USER_ID:
            random_code = f"KEY-{random.randint(1000000, 9999999)}"
            session_id = f"ADMIN_GEN_{int(time.time() * 1000)}"
            requests.put(f"{FIREBASE_URL}keys/{session_id}.json", json={"code": random_code, "type": "day"})
            send_message(chat_id, f"🛠️ **Tạo Key QTV thành công:** `{random_code}`")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
