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

# [2] 웹 서버 (Render 유지용)
app = Flask('')
@app.route('/')
def home(): return "K is listening."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True # <--- 이게 켜져 있어야 네 말을 들음!
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
        # 이 멘트가 나오면 성공이야!
        await channel.send("▶ **System switched to Chat Mode. Speak, Director.**")

# [6] 네가 말을 걸면 답장하는 기능
@client.event
async def on_message(message):
    if message.author == client.user: return # 내 말은 무시
    if message.channel.id != CHANNEL_ID: return # 다른 방 무시
    
    # 네가 말하면 로그에 찍힘 (디버깅용)
    print(f"📩 Message received from {message.author}: {message.content}")

    if ai_client:
        try:
            async with message.channel.typing():
                response = ai_client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"System: You are K, a cynical AI. Reply briefly.\nUser: {message.content}"
                )
                await message.channel.send(response.text)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send(f"Error: {e}")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
