import os
import json
import discord
from discord.ext import commands

# -----------------------------------------------------
# 設定とデータ管理
# -----------------------------------------------------

# 🚨 ピアボーナスを通知する専用チャンネルのIDに変更してください 🚨
BONUS_CHANNEL_ID = 123456789012345678 
POINTS_FILE = 'points.json'

# 環境変数からトークンを読み込む
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    print("エラー: 環境変数 DISCORD_TOKEN が設定されていません。")
    # ローカル実行時の代替として .env ファイルから読み込むなどの処理を追加できますが、
    # Railwayでのデプロイのためにここでは exit() します
    exit()

# -----------------------------------------------------
# ポイントデータの読み書き処理
# -----------------------------------------------------

def load_points():
    """ポイントデータをファイルから読み込む"""
    try:
        if os.path.exists(POINTS_FILE):
            with open(POINTS_FILE, 'r') as f:
                # ファイルから読み込んだキー(ユーザーID)をintに変換して返す
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
    except json.JSONDecodeError:
        print("警告: points.jsonの読み込みエラー。新しいファイルを作成します。")
        return {}
    return {}

def save_points(points_data):
    """ポイントデータをファイルに書き込む"""
    # 保存のためにユーザーIDを文字列に変換する
    with open(POINTS_FILE, 'w') as f:
        json.dump({str(k): v for k, v in points_data.items()}, f, indent=4)

# 起動時にポイントを読み込む
USER_POINTS = load_points()

def update_points(user_id, points):
    """ユーザーのポイントを更新し、ファイルを保存するヘルパー関数"""
    global USER_POINTS
    current_points = USER_POINTS.get(user_id, 0)
    USER_POINTS[user_id] = current_points + points
    save_points(USER_POINTS) # 更新のたびにファイルを保存
    return USER_POINTS[user_id]


# -----------------------------------------------------
# Botの初期設定
# -----------------------------------------------------

# メッセージ内容のインテントを有効にする (コマンド処理に必須)
intents = discord.Intents.default()
intents.message_content = True 

# コマンドプレフィックスを '!' に設定
bot = commands.Bot(command_prefix='!', intents=intents)


# -----------------------------------------------------
# イベント処理
# -----------------------------------------------------

@bot.event
async def on_ready():
    """BotがDiscordに接続したときに実行されます"""
    print(f'Botが起動しました。ログインユーザー: {bot.user}')


# --------------------------------