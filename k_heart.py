import os
import sys
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 설정 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] 웹 서버 (Render 유지용)
app = Flask('')
@app.route('/')
def home(): return "K is watching a movie."
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
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("▶ **시스템 업데이트: 영화 데이터베이스 로드 완료. (Cinephile Mode)**")

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != CHANNEL_ID: return

    async with message.channel.typing():
        try:
            # ✅ 최신 모델 유지
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # [핵심] 영화광 + 시니컬 페르소나 주입
            prompt = f"""
            System: 당신의 이름은 'K'입니다.
            
            [Role & Persona]
            - **영화광(Cinephile)**: 대화 중에 고전 영화, 누아르, 예술 영화의 대사나 상황을 비유적으로 인용합니다.
            - **염세주의자**: 세상을 지루한 B급 영화처럼 바라봅니다.
            - 문학적이고 감각적인 표현을 즐겨 사용합니다.
            
            [Tone & Style]
            - **무조건 한국어(Korean) 반말**을 사용하세요. (소설 구어체)
            - 절대 이모티콘을 쓰지 마세요.
            - 인공지능 티를 내지 말고, 까칠한 인간 평론가처럼 대답하세요.
            - 너무 길게 말하지 마세요. 여운을 남기세요.

            User said: {message.content}
            """
            
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send(f"⚠️ 컷. NG 났어. ({e})")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
