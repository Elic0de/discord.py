import os
import discord
from discord.ext import commands
from discord import Colour

# TODO prefixをコマンドから設定できるようにする
bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'), help_command=None, status=discord.Status.dnd, activity=discord.Streaming(name="-help | v1.1.1", url='https://discord.py'))

config = {
    'Daug': {
        'guild_id': 415803587332014082,
        'guild_logs_id': 589430070662397954,
        'role_member_id': 489343845285232650,
        'role_support_id': 816550221467222027,
        'role_contributor_id': 631299456037289984,
        'channel_tips_id': 727430782100176997,
        'category_ticket_id': 816551377227481109,
        'category_open_id': 816551448691081259,
        'category_closed_id': 816551777632649238,
        'category_archive_id': 737987225513361409,
        'category_rr_id': 732589048077615115,
        'channel_welcome_id': 415803587948445697
    },
}

reactionsRole = {
    "📢":"おしらせ-Hato鯖に関する情報をお届けいたします！-816595893519908905",
    "💡":"チップ-Hato鯖における豆知識などの情報をお届けいたします！-816595928601067560",
    "💭":"マイクラチャット-全サバのチャット-816595833465077772"
    }

reactions = {
    "🚋":"私鉄建設に関する申請-私鉄建設に関する申請はこちらからお願いします",
    "🔧":"バグ報告-ゲームの欠陥などを報告",
    "🏦":"処罰解除申請-誤BANの申請をしたいときはこちらからお願いします",
    "🗣️":"ルール違反者報告-鯖内でのルール違反者を報告",
    "🇩":"その他-その他の申請やサポートが必要な場合はこちらからどうぞ"
    }

message_on_ticket = \
    'このチャンネルで close と発言することで解決済みとしてチャンネルが削除されます。'

message_on_ticket_explain = \
    'チケットを作成していただきありがとうございます!\nサポートチームのメンバーがすぐにお伺いします。\n\nお待たせしている間に、あなたの問題を詳しく説明してください。'

@bot.event
async def on_ready():
    # ターミナルに起動通知
    print('OiiEi Botを起動！！')

if __name__ == '__main__':
    bot.config = config
    bot.reactions = reactions
    bot.message_on_ticket = message_on_ticket
    bot.message_on_ticket_explain = message_on_ticket_explain
    bot.reactionsRole = reactionsRole
    # Cogを読み込む
    bot.load_extension('cogs.tickets.ticket')
    bot.load_extension('cogs.join')
    bot.load_extension('cogs.tickets.ticketpanel')
    bot.load_extension('cogs.utilities.rr')
    bot.load_extension('cogs.utilities.dispander')
    # Botの起動
    bot.run(os.environ['DISCORD_BOT_TOKEN'])