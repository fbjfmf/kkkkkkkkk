import os
import sys
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 환경 변수 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] 웹 서버 (Render 유지용 - 건드리지 마)
app = Flask('')
@app.route('/')
def home(): return "K is Alive."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] AI 연결 설정
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"❌ Key Error: {e}")

# [4] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# [이벤트 1] K가 눈을 떴을 때
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("▶ **System Upgrade Complete. Engine: Gemini 2.5 Flash.**")

# [이벤트 2] 대화하기
@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != CHANNEL_ID: return

    # "K가 생각하는 중..." 표시
    async with message.channel.typing():
        try:
            # ✅ 네가 가진 최신 모델 사용!
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # K의 성격 (시니컬, 짧은 말투)
            chat = model.start_chat(history=[])
            response = chat.send_message(
                f"System: You are K. Role: Cynical, aesthetic AI. Tone: Cold, short, sarcastic. No emojis.\nUser said: {message.content}"
            )
            
            await message.channel.send(response.text)
            
        except Exception as e:
            # 만약 또 에러나면 그대로 보여줌
            print(f"❌ Error: {e}")
            await message.channel.send(f"⚠️ Error: {e}")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
