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
            title="役職パネル",
            url='',
            description="リアクションを押すと役職が自動的に付与されます。\n\n" + message,
            color=Colour.green().value)
        
    return embed

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.category_rr_id = self.bot.config['Daug']['category_rr_id']
        self.reactionsRole = self.bot.reactionsRole

    @commands.command()
    async def rrpanel(self, ctx):
        if ctx.channel.category_id != self.category_rr_id:
            return
        embed = get_panel(self.bot, self.reactionsRole)
        message = await ctx.send(embed=embed)
        await ctx.message.delete()

        for reaction in self.reactionsRole.keys():
            await message.add_reaction(reaction)    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):    
        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        guild = channel.guild
        reactions = self.reactionsRole

        if channel.guild.id != self.id:
            return
        if author.bot:
            return
        if channel.category_id != self.category_rr_id:
            return
        if not str(payload.emoji) in reactions.keys():
            return

        role = guild.get_role(int(reactions[str(payload.emoji)].split('-')[2]))
        await author.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        author = channel.guild.get_member(payload.user_id)
        guild = channel.guild
        reactions = self.reactionsRole

        if channel.guild.id != self.id:
            return
        if author.bot:
            return
        if channel.category_id != self.category_rr_id:
            return
        if not str(payload.emoji) in reactions.keys():
            return

        role = guild.get_role(int(reactions[str(payload.emoji)].split('-')[2]))
        await author.remove_roles(role)

def setup(bot):
    bot.add_cog(ReactionRole(bot))