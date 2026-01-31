import os
import sys
import asyncio
import random
from threading import Thread
from flask import Flask

# [생존 신고 1: 나 살아있다!]
print("🎬 SYSTEM: Script started...", flush=True)

try:
    import discord
    from google import genai # <--- 최신 라이브러리 확인!
    print("✅ SYSTEM: Libraries imported successfully.", flush=True)
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Library missing! {e}", flush=True)
    sys.exit(1) # 라이브러리 없으면 바로 종료 (로그에 남음)

# ==========================================
# [환경 변수 로드 & 검사]
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID_RAW = os.environ.get("CHANNEL_ID")

print(f"🔍 DEBUG: Key Length -> {len(GEMINI_API_KEY) if GEMINI_API_KEY else 'None'}", flush=True)
print(f"🔍 DEBUG: Token Length -> {len(DISCORD_TOKEN) if DISCORD_TOKEN else 'None'}", flush=True)

try:
    CHANNEL_ID = int(CHANNEL_ID_RAW)
    print(f"✅ DEBUG: Channel ID is valid: {CHANNEL_ID}", flush=True)
except:
    print(f"⚠️ WARNING: Channel ID '{CHANNEL_ID_RAW}' is invalid! Defaulting to 0.", flush=True)
    CHANNEL_ID = 0

# ==========================================
# [가짜 웹 서버: Render 생존용]
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "K is Alive."

def run_flask():
    # 포트 10000번 강제 고정
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# ==========================================
# [K의 본체]
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# AI 클라이언트 연결
ai_client = None
if GEMINI_API_KEY:
    try:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
        print("✅ SYSTEM: AI Client connected.", flush=True)
    except Exception as e:
        print(f"❌ ERROR: AI Connection failed: {e}", flush=True)

K_IDENTITY = "You are K. Cynical, aesthetic AI. Short sentences. No emojis."

async def think_and_speak():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    if not channel:
        print("❌ ERROR: Cannot find the channel. Check CHANNEL_ID.", flush=True)
        return

    await channel.send("*Connection re-established. The stage is set.*")
    print("🎬 K spoke: Connection re-established.", flush=True)

    while not client.is_closed():
        # 여기에 대화 로직...
        await asyncio.sleep(3600) # 1시간 대기

@client.event
async def on_ready():
    print(f'✅ LOGGED IN as {client.user}', flush=True)
    client.loop.create_task(think_and_speak())

# [실행 부스터]
if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        try:
            client.run(DISCORD_TOKEN)
        except Exception as e:
             print(f"❌ FATAL: Discord Login failed! {e}", flush=True)
    else:
        print("❌ FATAL: DISCORD_TOKEN is missing!", flush=True)
