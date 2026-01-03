from discord import Embed
from discord.ext import commands


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # PAGE 1
    # -------------------------
    @commands.command()
    async def help(self, ctx):
        embed = Embed(color=0xFFFFFF)

        embed.add_field(name="`!about`", value="Info about the bot and creator.", inline=False)
        embed.add_field(name="`!add LEV-ELC-ODE`", value="Add a level to the server's list.", inline=False)
        embed.add_field(name="`!remove LEV-ELC-ODE`", value="Remove one of your levels from the server's list.", inline=False)

        embed.add_field(name="`!addclearvid LEV-ELC-ODE URL`", value="Attach a clear video link to a level.", inline=False)
        embed.add_field(name="`!clearvid LEV-ELC-ODE`", value="Show the clear video for a level (if set).", inline=False)
        embed.add_field(name="`!removeclearvid LEV-ELC-ODE`", value="Remove your clear video from a level.", inline=False)

        embed.add_field(name="`!levelcount`", value="Show how many levels are stored for this server.", inline=False)
        embed.add_field(name="`!random`", value="Get a random level from the server's list.", inline=False)
        embed.add_field(name="`!mylevels`", value="List the levels you've submitted to this server.", inline=False)

        embed.add_field(name="`!register MAK-ERC-ODE`", value="Link your Discord account to your Maker ID.", inline=False)
        embed.add_field(name="`!unregister MAK-ERC-ODE`", value="Unlink a Maker ID from your account.", inline=False)
        embed.add_field(name="`!myid`", value="Show your registered Maker ID.", inline=False)

        embed.add_field(name="\u200b", value="---", inline=False)
        embed.set_footer(text="Page 1/2 • Next page: `!help2`")

        await ctx.send(embed=embed)

    # -------------------------
    # PAGE 2
    # -------------------------
    @commands.command()
    async def help2(self, ctx):
        embed = Embed(color=0xFFFFFF)

        embed.add_field(name="`!peek LEV-ELC-ODE`", value="Show an overworld image preview of the level.", inline=False)
        embed.add_field(name="`!viewer LEV-ELC-ODE`", value="Link to the Wizul SMM2 Level Viewer for a level.", inline=False)
        embed.add_field(
            name="`!viewersimple LEV-ELC-ODE`",
            value="Link to the viewer without calling the API.",
            inline=False,
        )

        embed.add_field(name="\u200b", value="---", inline=False)
        embed.set_footer(text="Page 2/2")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
