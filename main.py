import os
from fastapi import FastAPI, Request
import httpx
from dotenv import load_dotenv

from openai import OpenAI
import telebot
from github import Github, Auth

load_dotenv()

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


chatgpt = OpenAI(
    api_key=os.environ.get("OPEN_AI_KEY"),
)

access_token = os.getenv("GITHUB_TOKEN")
git_auth = Auth.Token(access_token)
git = Github(auth=git_auth)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['haiku'])
def chatgpt_handler(message):
    response = chatgpt.responses.create(
        model="gpt-4o-mini",
        input = "Write a short haiku"    
    )
    bot.reply_to(message, response.output_text)

user = git.get_user()
for repo in user.get_repos(affiliation="owner"):
    if repo.name == "Daily_problems":
        print(repo.name)
        commits = repo.get_commits()
        for commit in commits[:5]:  # Solo los 5 últimos
            print(f"Mensaje: {commit.commit.message}")
            print(f"Autor: {commit.commit.author.name}")
            print(f"Fecha: {commit.commit.author.date}")
            print("----")
            print(repo.name)

bot.infinity_polling()
