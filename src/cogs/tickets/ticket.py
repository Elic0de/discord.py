import discord
import time
from discord.ext import commands
from dispander import compose_embed
from ..module.embeds import compose_embed_default

async def change_category(channel, category) -> None:
    """チャンネルのカテゴリを変更"""
    await channel.edit(category=category)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.guild_logs_id = self.bot.config['Daug']['guild_logs_id']
        self.role_contributor_id = self.bot.config['Daug']['role_contributor_id']
        self.category_ticket_id = self.bot.config['Daug']['category_ticket_id']
        self.category_open_id = self.bot.config['Daug']['category_open_id']
        self.category_closed_id = self.bot.config['Daug']['category_closed_id']
        self.category_archive_id = self.bot.config['Daug']['category_archive_id']
        self.role_support_id = self.bot.config['Daug']['role_support_id']
        self.close_keywords = [
            'close', 'closes', 'closed',
            'fix', 'fixes', 'fixed',
            'resolve', 'resolves', 'resolved',
        ]
        self.message_on_ticket = self.bot.message_on_ticket
        self.message_on_ticket_explain = self.bot.message_on_ticket_explain


    async def dispatch_thread(self, message):
        category_open = message.guild.get_channel(self.category_open_id)
        if channels := [ch for ch in category_open.text_channels if str(message.author.id)[:6] in ch.name]:
            text = f'{message.author.mention} {channels[0].mention} こちらのサポートが未解決です。'
            resovleMessage = await message.channel.send(text)
            time.sleep(10)
            await resovleMessage.delete()
            await message.delete()
            return

        role_support =  message.guild.get_role(self.role_support_id)

        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True),
            role_support : discord.PermissionOverwrite(read_messages=True)
        }

        channel_support = await message.guild.create_text_channel(
            name=f"ticket-{str(message.author.id)[:6]}",
            topic=message.author.id,
            category=category_open,
            overwrites=overwrites
        )
    
        await channel_support.edit(position=0)
        await channel_support.send(embed=compose_embed_default(self.message_on_ticket_explain))
        await channel_support.send(embed=compose_embed_default(self.message_on_ticket))
        await message.channel.send(
            embed=compose_embed_default(
                f'チケットを {channel_support.mention} を作成しました {message.author.mention}')
        )

        title = await self.bot.wait_for(
            'message',
            check=lambda m: m.channel == channel_support
        )
        await self.dispatch_rename(title, title.content)

    async def dispatch_reopen(self, channel):
        await channel.edit(
            category=channel.guild.get_channel(self.category_open_id)
        )

    async def dispatch_close(self, channel):
        await channel.edit(
            category=channel.guild.get_channel(self.category_closed_id)
        )

    def is_category_open(self, channel):
        return channel.category_id == self.category_open_id

    def is_category_closed(self, channel):
        if channel.category is None:
            return False
        if '✅' in channel.category.name:
            return True
        if '🚫' in channel.category.name:
            return True
        return False


    def is_category_thread(self, channel):
        if self.is_category_open(channel):
            return True
        if self.is_category_closed(channel):
            return True
        return False

    async def dispatch_age(self, message):
        await message.channel.edit(
            position=0
        )

    async def dispatch_rename(self, message, rename):
        await message.channel.edit(name=rename)
        await message.channel.send(
            embed=compose_embed_default(f'チャンネル名を以下に変更しました\n{rename} ')
        )

    async def dispatch_archive(self, channel, member):
        category_archive = channel.guild.get_channel(self.category_archive_id)
        if channel.category.id == category_archive.id:
            if not member.guild_permissions.manage_channels:
                return
            # await transfer(
            #     channel_origin=channel,
            #     guild=self.bot.get_guild(self.guild_logs_id)
            # )
            await channel.delete()
        else:
            await change_category(channel, category_archive)
            return

    @commands.command()
    async def name(self, ctx, *, rename):
        message = ctx.message
        channel = ctx.message.channel
        conditions = (
            self.is_category_open(channel),
            self.is_category_closed(channel),
        )
        if not any(conditions):
            return
        await self.dispatch_rename(message, rename)

    @commands.command()
    async def archive(self, ctx):
        channel = ctx.channel
        author = ctx.author
        await self.dispatch_archive(channel, author)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        if message.guild.id != self.id:
            return
        if message.author.bot:
            return
        if not isinstance(channel, discord.channel.TextChannel):
            return
        ctx = await self.bot.get_context(message)
        if ctx.command:
            return
        if self.is_category_open(channel):
            if message.content in self.close_keywords:
                await self.dispatch_close(message.channel)
                return
            await self.dispatch_age(message)
        if channel.category_id == self.category_ticket_id:
            await self.dispatch_thread(message)
            return
        if self.is_category_closed(channel):
            await self.dispatch_reopen(channel)
            return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        
        if payload.guild_id != self.id:
            return
        if author.bot:
            return
        if payload.emoji.name == '✅':
            if not self.is_category_open(channel):
                return
            await self.dispatch_close(channel)
        if payload.emoji.name == '🚫':
            if not self.is_category_thread(channel):
                return
            await self.dispatch_archive(channel, author)

def setup(bot):
    bot.add_cog(Ticket(bot))