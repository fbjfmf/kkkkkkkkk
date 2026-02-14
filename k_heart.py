import os
import sys
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] 웹 서버
app = Flask('')
@app.route('/')
def home(): return "Diagnostic Mode"
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] AI 연결
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# [4] 디스코드 봇
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🕵️ **Diagnostic Mode ON. Say anything to list models.**")

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != CHANNEL_ID: return

    # 아무 말이나 걸면 작동
    await message.channel.send("🔄 **Checking API Permissions...**")

    try:
        available_models = []
        # [핵심] 현재 이 키로 쓸 수 있는 모든 모델을 조회함
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if available_models:
            # 모델 목록을 찾았으면 출력
            msg = "\n".join(available_models)
            await message.channel.send(f"✅ **Access Granted! Found these models:**\n```\n{msg}\n```\n👉 **Please copy one of these names exactly.**")
        else:
            # 목록이 비어있으면 키 문제
            await message.channel.send("❌ **Access Denied.** Your API Key has NO access to any models. Please check Google AI Studio.")

    except Exception as e:
        # 에러가 나면 그대로 출력
        await message.channel.send(f"🚨 **CRITICAL ERROR:**\n`{e}`")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
