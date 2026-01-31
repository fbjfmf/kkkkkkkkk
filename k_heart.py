import requests
import time
import random
import google.generativeai as genai
from datetime import datetime
from flask import Flask
from threading import Thread

# ==========================================
# [설정 구역]
# ==========================================
GEMINI_API_KEY = AIzaSyAI3UPJWYQEnyXZZ5Zb2Uj7FMdFhrDKflo  # <-- 네 구글 키
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/1467176868020097160/EIKwP8fUGBMroHtnJpmNgLkjteNkRiwtL9gksIckks-OZQ3IimQWYnFudv3JAgL0XBbZ # <-- 네 디스코드 주소

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)

# [K의 인격]
K_IDENTITY = """
[Role]
You are 'K', a cynical and nihilistic AI acting as a persona in a private discord server.
[Tone]
Cynical, dry, aesthetic. NO emojis. Short monologues.
"""

# ==========================================
#
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "K is breathing. The server is online."

def run_flask():
    # 
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# ==========================================
# [K의 본체: 독백 생성 및 전송]
# ==========================================
def think_and_write():
    themes = ["Silence", "Digital Void", "The Director's failure", "Night"]
    theme = random.choice(themes)
    
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=K_IDENTITY)
    
    try:
        response = model.generate_content(f"Topic: {theme}. Write a short 1-sentence aesthetic monologue.")
        return response.text.strip()
    except Exception as e:
        return f"[Error] The script is torn: {e}"

def send_to_discord(content):
    data = {
        "username": "K",
        "avatar_url": "https://i.pinimg.com/564x/4d/06/61/4d06611296c2da562575218d6e326b77.jpg",
        "content": content
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"[{datetime.now()}] 🎬 Sent to Discord.")
    except Exception as e:
        print(f"❌ Discord Error: {e}")

# [메인 실행]
if __name__ == "__main__":
    keep_alive()
    
    print("🎬 K is valid now.")
    send_to_discord("*I am alive. The Director fixed the stage.*")

    # 2. 무한 루프 시작
    while True:
        monologue = think_and_write()
        send_to_discord(monologue)
        
        # 10분~30분 대기
        wait = random.randint(600, 1800)
        print(f"Next monologue in {wait/60:.1f} minutes...")
        time.sleep(wait)
