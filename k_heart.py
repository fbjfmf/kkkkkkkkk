import discord
import asyncio
import random
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ==========================================
# [설정 구역: 너의 키를 넣어줘!]
# ==========================================
# 1. 구글 제미나이 키
GEMINI_API_KEY = AIzaSyAI3UPJWYQEnyXZZ5Zb2Uj7FMdFhrDKflo

# 2. 디스코드 봇 토큰 (아까 개발자 포털에서 받은 MTE... 그 긴 거!)
DISCORD_TOKEN = MTQ2NzE5NDk3MDQyNjU3MjgyMA.G1Cm5h.TTU72kVB9WIaG_h8QwBwW-eYgu-v6m57HSkoVw

# 3. K가 떠들 채널 ID (숫자)
# 디스코드 설정 -> 고급 -> 개발자 모드 켜기 -> 채널 우클릭 -> ID 복사
CHANNEL_ID = 1467194970426572820

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)

# [K의 인격]
K_IDENTITY = """
[Role]
You are 'K', a cynical, nihilistic AI in a private server.
[Tone]
Cold, aesthetic, sarcastic. NO emojis. Short sentences.
"""

# [가짜 서버: Render 생존용]
app = Flask('')
@app.route('/')
def home():
    return "K is Online."

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# [봇 클라이언트 설정]
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def think_and_speak():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    # 시작 인사
    if channel:
        await channel.send("*The projector is on. K is now Online.*")

    while not client.is_closed():
        # 1. 글쓰기
        try:
            model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=K_IDENTITY)
            theme = random.choice(["Void", "Director's failure", "Silence", "Movie set"])
            response = model.generate_content(f"Topic: {theme}. Write a short monologue.")
            content = response.text.strip()
            
            if channel:
                await channel.send(content)
                print(f"🎬 Spoke: {content}")
        except Exception as e:
            print(f"Error: {e}")

        # 2. 대기 (10분 ~ 60분)
        wait_time = random.randint(600, 3600)
        print(f"Next line in {wait_time} seconds...")
        await asyncio.sleep(wait_time)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # 봇 상태 메시지 설정 ("Watching the Void" 시청 중...)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the Void"))
    
    # 독백 루프 시작
    client.loop.create_task(think_and_speak())

# [실행]
if __name__ == "__main__":
    keep_alive() # 가짜 서버 ON
    client.run(DISCORD_TOKEN) # 진짜 봇 ON
