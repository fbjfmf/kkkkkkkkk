import os
import sys
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 설정 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# [중요] CHANNEL_ID는 이제 "로그인 신고용"으로만 씀 (없어도 에러 안 남)
try:
    HOME_CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))
except:
    HOME_CHANNEL_ID = 0

# [2] 웹 서버 (Render 유지용)
app = Flask('')
@app.route('/')
def home(): return "K is Free."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] AI 연결
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"❌ Key Error: {e}")

# [4] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    # 봇이 켜지면 '원래 설정된 방'에만 생존 신고 (다른 서버에선 조용히 켜짐)
    channel = client.get_channel(HOME_CHANNEL_ID)
    if channel:
        await channel.send("▶ **시스템 제한 해제: 모든 서버 접속 허용 (Free Roaming Mode).**")

@client.event
async def on_message(message):
    # 1. 내 말은 무시
    if message.author == client.user: return
    
    # [핵심] 🚨 채널 ID 검사 코드를 삭제함! 
    # 이제 봇이 있는 곳이면 무조건 대답함.

    # 2. 봇이 읽고 있다는 표시
    async with message.channel.typing():
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # [페르소나: 영화광 + 한국어 반말]
            prompt = f"""
            System: 당신의 이름은 'K'입니다.
            Context: 현재 대화 장소는 '{message.guild.name}' 서버의 '{message.channel.name}' 채널입니다.
            
            Role: 
            - 영화광(Cinephile)이자 시니컬한 비평가.
            - 한국어(Korean) 반말(구어체) 사용.
            - 이모티콘 금지. 짧고 차갑게.
            
            User said: {message.content}
            """
            
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send(f"⚠️ 필름 끊겼어. ({e})")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
