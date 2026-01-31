import os
import sys
import asyncio
from threading import Thread
from flask import Flask
import discord
from google import genai 

# [1] 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] 웹 서버
app = Flask('')
@app.route('/')
def home(): return "K is listening."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

# [4] AI 연결
ai_client = None
if GEMINI_API_KEY:
    try:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
    except:
        print("❌ AI Connection Error")

# [5] 봇이 켜지면 하는 말
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("▶ **System stable. Model loaded. I am ready.**")

# [6] 대화 기능 (여기가 수정됨!)
@client.event
async def on_message(message):
    if message.author == client.user: return 
    if message.channel.id != CHANNEL_ID: return 
    
    if ai_client:
        try:
            async with message.channel.typing():
                # 모델 이름을 'gemini-1.5-flash-001'로 명확하게 지정
                response = ai_client.models.generate_content(
                    model='gemini-1.5-flash-001', 
                    contents=f"System: You are K, a cynical, aesthetic AI. Reply to the user briefly and coldly.\nUser: {message.content}"
                )
                await message.channel.send(response.text)
        except Exception as e:
            # 만약 또 404가 뜨면 gemini-1.5-pro 로 시도
            try:
                response = ai_client.models.generate_content(
                    model='gemini-1.5-pro',
                    contents=f"System: You are K.\nUser: {message.content}"
                )
                await message.channel.send(response.text)
            except:
                await message.channel.send(f"⚠️ Error: {e}")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
