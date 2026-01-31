import discord
import asyncio
import random
import google.generativeai as genai
import os  # <--- 이 친구가 필요해!
from flask import Flask
from threading import Thread

# ==========================================
# 
# ==========================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID")) 

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)
