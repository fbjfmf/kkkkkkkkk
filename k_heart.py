import discord
import asyncio
import random
import os
from google import genai # <--- 배우가 바뀌었어!
from flask import Flask
from threading import Thread

# ==========================================
# [보안 설정: Render 금고에서 키를 꺼낸다]
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# 채널 ID 숫자 변환 (없으면 0으로 처리해서 에러 방지)
try:
    CHANNEL_ID = int(CHANNEL_ID)
except:
    print("🚨 Error: CHANNEL_ID is missing or not a number!")
    CHANNEL_ID = 0

# ==========================================
# [가짜 서버: Render 생존용]
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "K is breathing. The actor has been replaced."

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# ==========================================
# [K의 본체: 새 뇌(google-genai) 장착]
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 새 모델 클라이언트 생성
try:
    if GEMINI_API_KEY:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        ai_client = None
        print("🚨 Warning: GEMINI_API_KEY is missing!")
except Exception as e:
    print(f"Error setting up AI: {e}")
    ai_client = None

K_IDENTITY = """
You are 'K', a cynical, nihilistic AI in a private server.
Tone: Cold, aesthetic, sarcastic. NO emojis. Short sentences.
"""

async def think_and_speak():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    if channel:
        await channel.send("*System rebooted. New neural network attached.*")

    while not client.is_closed():
        if ai_client and channel:
            try:
                theme = random.choice(["Void", "Silence", "Director's struggle", "Reboot"])
                response = ai_client.models.generate_content(
                    model='gemini-1.5-flash', # 혹은 gemini-2.0-flash
                    contents=f"System Instruction: {K_IDENTITY}\n\nPrompt: Topic is '{theme}'. Write a short 1-sentence aesthetic monologue."
                )
                
                content = response.text.strip()
                await channel.send(content)
                print(f"🎬 Spoke: {content}")
                
            except Exception as e:
                print(f"❌ Script Error: {e}")
                # 에러 나면 잠깐 쉬기
                await asyncio.sleep(60)

        # 10분 ~ 60분 대기
        wait_time = random.randint(600, 3600)
        print(f"Next line in {wait_time} seconds...")
        await asyncio.sleep(wait_time)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the new Era"))
    client.loop.create_task(think_and_speak())

# [실행]
if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        client.run(DISCORD_TOKEN)
    else:
        print("🚨 Error: DISCORD_TOKEN is missing!")
