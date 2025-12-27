from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Update
from datetime import datetime

app = FastAPI()

# --- CONFIGURATION (Hardcoded for Test Scenario) ---
# ⚠️ SECURITY WARNING: Never commit this file to a public GitHub repo
# while it contains the real token.
TOKEN = "7739387192:AAHoiEu73mp89GV29CUvbODM9LZdPI3nmpg" 
WEBHOOK_SECRET = "my-secret-test-123" 

# Initialize Bot and Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- BOT LOGIC ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"🕒 The current server time is: {current_time}")

# --- WEBHOOK HANDLER ---
@app.post("/webhook")
async def telegram_webhook(request: Request):
    # verify secret token from Telegram headers
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != WEBHOOK_SECRET:
        return {"status": "unauthorized"}

    # Process update
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Error: {e}")
        
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Bot is running on Vercel"}