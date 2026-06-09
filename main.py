import os
import base64
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 
API_HASH = ""
BOT_TOKEN = "8523816033:_5gbXlM93sqeywVnPtiAylc"

API_URL = "https://gemini-aistudio-audio-automator.onrender.com/request"

app = Client(
    "gemini_tts_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

VOICE = "Zephyr"
SCENE = "friendly"

@app.on_message(filters.command(["start"]))
async def start(_, message: Message):
    await message.reply_text(
        "Send:\n\n/tts Hello World"
    )

@app.on_message(filters.command(["tts"]))
async def tts(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/tts your text"
        )

    text = message.text.split(None, 1)[1]

    msg = await message.reply_text("Generating audio...")

    try:
        r = requests.post(
            API_URL,
            json={
                "prompt": text,
                "voice": VOICE,
                "scene": SCENE
            },
            timeout=300
        )

        data = r.json()

        if data.get("status") != "success":
            return await msg.edit("Generation failed.")

        audio_data = data.get("audio")

        if not audio_data:
            return await msg.edit("No audio returned.")

        audio_bytes = base64.b64decode(audio_data)

        filename = f"tts_{message.id}.wav"

        with open(filename, "wb") as f:
            f.write(audio_bytes)

        await message.reply_audio(
            filename,
            title="Gemini AI Studio TTS"
        )

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit(f"Error:\n{e}")

app.run()
