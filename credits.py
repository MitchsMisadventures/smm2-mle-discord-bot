from discord import Embed
from discord.ext import commands

class CreditCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        embed = Embed(
            title="Mitch's Level Exchange",  
            description=(
                "Thank you for downloading Mitch's Level Exchange! This bot allows you to share and discover "
                "Super Mario Maker 2 levels right here on Discord. "
                "For more information, just use the `/help` command to get started."
            ),
            color=0xFFFFFF
        )
        embed.add_field(name="Contact", value="Feel free to follow me on Twitter: @MitchsMisplays\n "
                                              "Subscribe to me on Youtube @MitchsMisadventures", inline=False)  
        
        embed.add_field(name="Support The Bot", value="If you want to support me and/or the bot, consider sparing some change by clicking this link!\n\n"
                                                      "This of course is **NOT REQUIRED** and does not give any extra benefits.")

        embed.add_field(name="Version", value="1.0", inline=False)  

        await ctx.send(embed=embed)

    @commands.command()
    async def changelog(self, ctx):
        embed = Embed(
            title="Changelog",  
            color=0x1EFF90
        )

        embed.add_field(name="Version 1.0", value="First release!", inline=False)  

        embed.add_field(name="\u200b", value = "___",inline = False)

        embed.set_footer(text="For the full changelog, click here!")

        await ctx.send(embed = embed)

    @commands.command()
    async def helpme(self, ctx):
        embed = Embed(
            color=0xA3A3A3
        )

        embed.add_field(name="/register MAK-ERC-ODE", value="Register your Maker ID to your Discord!", inline=False)

        embed.add_field(name="/unregister MAK-ERC-ODE", value="Unregister your Maker ID from your Discord.", inline=False)

        embed.add_field(name="/myid", value="Receive your Maker ID linked to your Discord.", inline=False)

        embed.add_field(name="/about", value="Get most recent Bot information.", inline=False)  

        embed.add_field(name="/changelog", value = "Get Bot changelog and history.",inline = False)

        embed.add_field(name="/helpme", value = "You know what this does, lol.",inline = False)

        embed.add_field(name="\u200b", value = "___",inline = False)

        embed.set_footer(text="Page 1.")

        await ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(CreditCommands(bot))
