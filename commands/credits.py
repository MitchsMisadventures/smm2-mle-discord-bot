from discord import Embed
from discord.ext import commands


class CreditCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # BOT CREDITS / ABOUT
    # -------------------------
    @commands.command()
    async def about(self, ctx):
        embed = Embed(
            title="Mitch's Level Exchange",
            description=(
                "Thanks for using Mitch's Level Exchange! This bot lets you share and discover "
                "Super Mario Maker 2 levels right here on Discord.\n\n"
                "For help with commands, use `!help`."
            ),
            color=0xFFFFFF,
        )

        embed.add_field(
            name="Contact",
            value=(
                "Follow me on Twitter: **@MitchsMisplays**\n"
                "YouTube: **@MitchsMisadventures**"
            ),
            inline=False,
        )

        embed.add_field(
            name="Support The Bot",
            value=(
                "If you want to support me and/or the bot, you can leave a tip here:\n"
                "https://streamelements.com/mitchsmisplays/tip\n\n"
                "This is **not required** and does not unlock extra benefits."
            ),
            inline=False,
        )

        embed.add_field(name="Version", value="1.0", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CreditCommands(bot))
