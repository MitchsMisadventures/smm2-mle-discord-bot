from discord.ext import commands

class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx):
        await ctx.send("Hello, this test worked.")

    @commands.command()
    async def remove(self, ctx):
        await ctx.send("!test")

    @commands.command()
    async def clearvideo(self, ctx):
        await ctx.send('Bottom Jeans!')

    @commands.command()
    async def random(self, ctx):
        await ctx.send('Bottom Jeans!')

    @commands.command()
    async def like(self, ctx):
        await ctx.send('Bottom Jeans!')

async def setup(bot):
    await bot.add_cog(LevelCommands(bot))
