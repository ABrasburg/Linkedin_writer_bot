import os
from fastapi import FastAPI, Request
from openai import OpenAI
import telebot
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(
    api_key=os.environ.get("OPEN_AI_KEY"),
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['haiku'])
def chatgpt_handler(message):
    response = client.responses.create(
        model="gpt-4o-mini",
        input = "Write a short haiku"    
    )
    bot.reply_to(message, response.output_text)

bot.infinity_polling()