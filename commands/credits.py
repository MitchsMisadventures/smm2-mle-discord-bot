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


async def setup(bot):
    await bot.add_cog(CreditCommands(bot))
