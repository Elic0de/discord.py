import discord
import sys
from discord.ext import commands
sys.path.append('../')
from hato.card_generator import generate_card

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.role_member_id = self.bot.config['Daug']['role_member_id']

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != self.id:
            return
        if member.bot:
            return
        await ctx.author.avatar_url.save('hato/icon.png')
        generate_card(ctx.author)
        await ctx.send(file=discord.File('hato/card.png'))
        role_member = member.guild.get_role(self.role_member_id)
        await member.add_roles(role_member)
    
    @commands.command()
    async def card(self, ctx):
        await ctx.author.avatar_url.save('hato/icon.png')
        generate_card(ctx.author)
        await ctx.send(file=discord.File('hato/card.png'))

def setup(bot):
    bot.add_cog(Join(bot))