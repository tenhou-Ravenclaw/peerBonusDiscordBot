import os
import discord
from discord.ext import commands
# ... 他のimport

# 環境変数からトークンを読み込むように修正
# Renderで設定する環境変数名に合わせてください（ここでは DISCORD_TOKEN を想定）
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    print("エラー: 環境変数 DISCORD_TOKEN が設定されていません。")
    exit()

# コマンドのプレフィックス（例: !）を設定
intents = discord.Intents.default()
intents.message_content = True # コマンドを処理するために必要
bot = commands.Bot(command_prefix='!', intents=intents)

# ... ピアボーナスのコマンド定義（@bot.command() など） ...

@bot.event
async def on_ready():
    print(f'Botが起動しました。ログインユーザー: {bot.user}')

# Botを起動
bot.run(DISCORD_TOKEN)