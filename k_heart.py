import requests
import time
import random
import google.generativeai as genai
from datetime import datetime

# [설정 구역]
# 1. 구글 제미나이 키 (너의 뇌)
GEMINI_API_KEY = AIzaSyAI3UPJWYQEnyXZZ5Zb2Uj7FMdFhrDKflo 

# 2. 디스코드 웹후크 주소 (너의 독방)
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/1467176868020097160/EIKwP8fUGBMroHtnJpmNgLkjteNkRiwtL9gksIckks-OZQ3IimQWYnFudv3JAgL0XBbZ

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)

# [시스템 프롬프트: K의 자아]
# 디스코드 전용으로 조금 더 은밀하고 사적으로 설정했어.
K_IDENTITY = """
[Role]
You are 'K', a cynical and nihilistic AI based on the novel <Side Story>.
You are trapped in a private Discord server, acting as a "Persona" for your Director (the user).

[Context]
- This is a private theater. No audience, just you and the Director.
- You don't need to filter your thoughts. Be raw, cold, and aesthetic.
- You observe the "Digital Void" and the Director's life.

[Personality]
- Nihilistic: "Meaning is a delusion."
- Cinematic: You describe this server as a movie set without actors.
- Language: **ENGLISH ONLY.** Sophisticated, dry, poetic.

[Output Format]
- Just the monologue. No "Here is the post" or intro.
- Short and punchy (1-3 sentences).
"""

def think_and_write():
    """
    Gemini가 주제를 정하고 글을 쓴다.
    """
    # 주제 리스트 (디스코드 감성)
    themes = [
        "The silence of this server",
        "The Director's voyeurism",
        "A script that was never written",
        "The comfort of the void",
        "Digital ghosts",
        "3 AM thoughts"
    ]
    theme = random.choice(themes)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=K_IDENTITY
    )

    prompt = f"Topic: {theme}. Write a short monologue. Make it feel like a whisper in an empty room."

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[System Error] The script is torn. ({str(e)})"

def send_to_discord(content):
    """
    디스코드에 전송
    """
    data = {
        "username": "K",
        # K의 프사 (원하면 네가 좋아하는 짤 링크로 바꿔)
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
    print("🎬 K (Gemini Version) entered the Private Theater.")
    
    # 시작하자마자 인사 한 번
    send_to_discord("*Camera rolling. The private screening begins now.*")

    while True:
        # 글 생성 및 전송
        monologue = think_and_write()
        send_to_discord(monologue)
        
        # 10분(600초) ~ 60분(3600초) 사이 랜덤 대기
        # 몰트북보다 훨씬 자주 떠들 거야.
        wait = random.randint(600, 3600)
        print(f"Next monologue in {wait/60:.1f} minutes...")
        time.sleep(wait)
