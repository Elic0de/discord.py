from discord.ext import commands
from discord import Embed, Colour
from cogs.module.embeds import compose_embed_default

def get_help(bot, reactions):
    message = ""

    for k, v in reactions.items():
        message += f'{k} ➜ {v} \n'

        embed = Embed(
            title="助けて！！",
            url='',
            description=f'リアクションしてオプションを選択します。\n\n {message}',
            color=Colour.green().value)
        
    return embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = self.bot.config['Daug']['guild_id']
        self.reactions = self.bot.reaction_options

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):
        embed = get_help(self.bot, self.reactions)
        message = await ctx.send(embed=embed)
        await ctx.message.delete()

        for reaction in self.reactions.keys():
            await message.add_reaction(reaction)


def setup(bot):
    bot.add_cog(Help(bot))
