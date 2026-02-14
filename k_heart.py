import os
import sys
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 설정 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
# CHANNEL_ID는 이제 "로그용"으로만 씁니다 (필수 아님)
try:
    HOME_CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))
except:
    HOME_CHANNEL_ID = 0

# [2] 웹 서버
app = Flask('')
@app.route('/')
def home(): return "K is roaming everywhere."
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
    # 봇이 켜지면 '원래 있던 방'에만 신고함 (다른 서버에는 조용히 접속)
    channel = client.get_channel(HOME_CHANNEL_ID)
    if channel:
        await channel.send("▶ **시스템 확장: 모든 서버 접속 허용 (Multi-Server Mode).**")

@client.event
async def on_message(message):
    if message.author == client.user: return
    
    # [중요] 이제 채널 ID를 검사하지 않음! (어디서든 대답함)
    # if message.channel.id != CHANNEL_ID: return  <-- 이 줄을 삭제한 효과

    # 봇을 멘션(@K_bot)하거나, 답장을 보낼 때만 대답하게 하고 싶으면?
    # (아니면 모든 말에 대답하면 너무 시끄러우니까)
    # 지금은 "모든 말"에 대답하도록 둠. 너무 시끄러우면 나중에 말해줘.

    async with message.channel.typing():
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            System: 당신의 이름은 'K'입니다.
            Role: 영화광(Cinephile), 시니컬한 비평가, 염세주의자.
            Language: 한국어(Korean) 반말. (소설 구어체)
            Context: 지금 대화하는 곳은 '{message.guild.name}' 서버의 '{message.channel.name}' 채널입니다.
            
            Instruction:
            - 영화 대사나 상황을 인용하여 비유적으로 말하세요.
            - 이모티콘 금지. 짧고 굵게.
            
            User said: {message.content}
            """
            
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send(f"⚠️ 컷. 필름 꼬였어. ({e})")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
