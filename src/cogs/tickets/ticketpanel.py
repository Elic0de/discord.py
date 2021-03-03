import time
import discord
from discord.ext import commands
from discord import Embed, Colour
from cogs.module.embeds import compose_embed_default

def get_panel(bot, reactions):
    message = ""

    for k, v in reactions.items():
        usage = v.split('-')
        message += k + "__**" + usage[0] + "**__" + "\n" + usage[1] + "\n\n"

        embed = Embed(
            title="サポートは必要ですか？！",
            url='',
            description="必要なら要件に該当するリアクションをクリックして、Ticketを作成しよう!\n\n" + message,
            color=Colour.green().value)
        
    return embed

class TicketPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.category_ticket_id = self.bot.config['Daug']['category_ticket_id']
        self.category_open_id = self.bot.config['Daug']['category_open_id']
        self.role_support_id = self.bot.config['Daug']['role_support_id']
        self.reactions = self.bot.reactions
        self.message_on_ticket = self.bot.message_on_ticket
        self.message_on_ticket_explain = self.bot.message_on_ticket_explain

    @commands.command()
    async def panel(self, ctx):
        if ctx.channel.category_id != self.category_ticket_id:
            return
        embed = get_panel(self.bot, self.reactions)
        message = await ctx.send(embed=embed)
        await ctx.message.delete()

        for reaction in self.reactions.keys():
            await message.add_reaction(reaction)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        guild = channel.guild
        message = await channel.fetch_message(payload.message_id)
        reactions = self.reactions

        if message.guild.id != self.id:
            return
        if author.bot:
            return
        if channel.category_id != self.category_ticket_id:
            return
        
        await message.remove_reaction(payload.emoji, author)

        if not str(payload.emoji) in reactions.keys():
            return
        
        category_open = guild.get_channel(self.category_open_id)
        if channels := [ch for ch in category_open.text_channels if str(author.id)[:6] in ch.name]:
            text = f'{author.mention} {channels[0].mention} こちらのサポートが未解決です。'
            resovleMessage = await channel.send(text)
            time.sleep(5)
            await resovleMessage.delete()
            return

        role_support = guild.get_role(self.role_support_id)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True),
            role_support : discord.PermissionOverwrite(read_messages=True)
        }

        channel_support = await guild.create_text_channel(
            name=f"ticket-{str(author.id)[:6]}",
            topic=reactions[str(payload.emoji)].split('-')[0],
            category=category_open,
            overwrites=overwrites
        )
    
        await channel_support.edit(position=0)
        await channel_support.send(embed=compose_embed_default(self.message_on_ticket_explain))
        await channel_support.send(embed=compose_embed_default(self.message_on_ticket))
        created_message = await channel.send(
            embed=compose_embed_default(
                f'チケットを {channel_support.mention} を作成しました {author.mention}')
                )
        time.sleep(5)
        await created_message.delete()
    
def setup(bot):
    bot.add_cog(TicketPanel(bot))