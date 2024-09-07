from discord import Embed
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

### PAGE 1 OF COMMANDS ###

    @commands.command()
    async def help(self, ctx):
        embed = Embed(
            color=0xFFFFFF
        )

        embed.add_field(name="`!about`", value="Returns general infomration about bot and creator!", inline=False)

        embed.add_field(name="`!add LEV-ELC-ODE`", value="Allows you to add a level to the server's list!", inline=False)

        embed.add_field(name="`!addclearvid LEV-ELC-ODE URL`", value="Allows you to add a clear video to a level from the server.", inline=False)

        embed.add_field(name="`!clearvid LEV-ELC-ODE`", value="Recalls Clear Video to a level if one is set.", inline=False)

        embed.add_field(name="`!help`", value="Returns Page 1 of available bot commmands.", inline=False)

        embed.add_field(name="`!help2`", value="Returns Page 2 of available bot commands.", inline=False)

        embed.add_field(name="`!levelcount`", value="Returns count of levels currently stored on the server.", inline=False)

        embed.add_field(name="`!myid`", value="Returns a list of levels User has submitted to the server.", inline=False)

        embed.add_field(name="`!mylevels`", value="Returns a list of levels User has submitted to the server.", inline=False)

        embed.add_field(name="`!register MAK-ERC-ODE`", value = "Allows you to link Discord user with Super Mario Maker 2 Maker ID.",inline = False)

        embed.add_field(name="\u200b", value = "---",inline = False)

        embed.set_footer(text="Page 1/2. For next page, do /help2")

        await ctx.send(embed = embed)

### PAGE 2 OF COMMANDS ###

    @commands.command()
    async def help2(self, ctx):
        embed = Embed(
            color=0xFFFFFF
        )

        embed.add_field(name="`!peek LEV-ELC-ODE`", value="Returns an image of the full overworld of a level.", inline=False)

        embed.add_field(name="`!random`", value="Returns a random level from the server's level list.", inline=False)  

        embed.add_field(name="`!remove LEV-ELC-ODE`", value="Removes level from server list.", inline=False)

        embed.add_field(name="`!removeclearvid LEV-ELC-ODE`", value="Removes a Clear Video from a level if one is already assigned to it.", inline=False)

        embed.add_field(name="`!unregister`", value="Allows you to unlink Discord user with Super Mario Maker 2 Maker ID.", inline=False)

        embed.add_field(name="`!viewer LEV-ELC-ODE`", value="Returns a direct link to the Wizul SMM2 Level Viewer for given level.", inline=False)

        embed.add_field(name="`!viewersimple LEV-ELC-ODE`", value="Returns a direct link to the Wizul SMM2 Level Viewer for given level *without* accessing API.", inline=False)

        embed.add_field(name="\u200b", value = "---",inline = False)

        embed.set_footer(text="Page 2/2")

        await ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
