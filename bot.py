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

# -----------------------------------------------------
# ピアボーナス機能の追加
# -----------------------------------------------------

# 簡易的なポイントデータストア (注意: Bot再起動で消えます!)
# 安定稼働には外部DBが必要ですが、テストのためローカル辞書を使用
USER_POINTS = {}

# ポイント付与とチャンネル通知のチャンネルID (🚨ご自身のIDに変更してください🚨)
BONUS_CHANNEL_ID = 123456789012345678 # 例: '998877665544332211' などの専用チャンネルID

def update_points(user_id, points):
    """ユーザーのポイントを更新するヘルパー関数"""
    current_points = USER_POINTS.get(user_id, 0)
    USER_POINTS[user_id] = current_points + points
    return USER_POINTS[user_id]


@bot.command(name='thank')
async def give_bonus(ctx, member: discord.Member, *, reason: str = "特に理由なし"):
    """
    ピアボーナスを付与するコマンド: !thank @ユーザー 理由
    """
    # 1. 自分自身を褒めるのをチェック
    if member.id == ctx.author.id:
        await ctx.send(f"❌ {ctx.author.display_name}さん、自分自身を褒めることはできません！")
        return

    # 2. ポイント付与
    # 褒めた人: 1点
    update_points(ctx.author.id, 1)
    # 褒められた人: 2点
    update_points(member.id, 2)

    # 3. 専用チャンネルへの投稿
    bonus_channel = bot.get_channel(BONUS_CHANNEL_ID)

    if bonus_channel:
        # メッセージを作成
        embed = discord.Embed(
            title="🌟 ピアボーナス付与！",
            description=f"**{ctx.author.display_name}** さんが **{member.display_name}** さんを褒めました！",
            color=discord.Color.gold()
        )
        embed.add_field(name="理由", value=reason, inline=False)
        embed.add_field(name="ポイント内訳", value=f"✅ 褒めた人 ({ctx.author.display_name}): **+1** 点\n✅ 褒められた人 ({member.display_name}): **+2** 点", inline=False)
        
        await bonus_channel.send(embed=embed)
        
        # コマンドを実行したチャンネルへの確認メッセージ
        await ctx.send(f"✅ ボーナスを付与しました！確認は <#{BONUS_CHANNEL_ID}> でどうぞ。")
    else:
        # チャンネルが見つからない場合は、実行チャンネルに通知
        await ctx.send(f"✅ ボーナスを付与しました！しかし、設定されたチャンネルID({BONUS_CHANNEL_ID})が見つかりません。")

# -----------------------------------------------------