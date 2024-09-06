from discord import Embed
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = Embed(
            color=0xFFFFFF
        )

        embed.add_field(name="`/register MAK-ERC-ODE`", value="Register your Maker ID to your Discord!", inline=False)

        embed.add_field(name="`/unregister MAK-ERC-ODE`", value="Unregister your Maker ID from your Discord.", inline=False)

        embed.add_field(name="`/add LEV-ELC-ODE`", value="Add Level to database!", inline=False)

        embed.add_field(name="`/remove LEV-ELC-ODE`", value="Removes level from database!", inline=False)

        embed.add_field(name="`/addclearvid LEV-ELC-ODE URL`", value="Adds clear video to level in database.", inline=False)

        embed.add_field(name="`/removeclearvid LEV-ELC-ODE`", value="Removes clear video from level in database.!", inline=False)

        embed.add_field(name="`/clearvid LEV-ELC-ODE`", value="Calls clear video for specified level.", inline=False)

        embed.add_field(name="`/myid`", value="Receive your Maker ID linked to your Discord.", inline=False)

        embed.add_field(name="`/about`", value="Get most recent Bot information.", inline=False)  

        embed.add_field(name="`/help`", value = "You know what this does, lol.",inline = False)

        embed.add_field(name="\u200b", value = "---",inline = False)

        embed.set_footer(text="Page 1/2. For next page, do /help2")

        await ctx.send(embed = embed)

    @commands.command()
    async def help2(self, ctx):
        embed = Embed(
            color=0xFFFFFF
        )

        embed.add_field(name="`/mylevels`", value="Show all of my levels submitted.", inline=False)

        embed.add_field(name="`/viewall`", value="View all levels in server.", inline=False)

        embed.add_field(name="`/viewer LEV-ELC-ODE`", value="Pull online Level Viewer link for level.", inline=False)

        embed.add_field(name="`/viewlevel LEV-ELC-ODE`", value="Paste full png image of level into chat.", inline=False)

        embed.add_field(name="\u200b", value = "---",inline = False)

        embed.set_footer(text="Page 2/2")

        await ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
