from discord import Embed, User
from discord.ext import commands
import re
import requests


class ViewerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # GETTING OVERWORLD THUMBNAIL
    # -------------------------
    @commands.command()
    async def peek(self, ctx, code: str = None, user: User = None):
        if not code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(name=" ", value="Incorrect format. Try `!peek LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value="Invalid code format. Please use the format `!peek LEV-ELC-ODE` or `!peek LEVELCODE`.",
            )
            await ctx.send(embed=embed)
            return

        json_code = self.get_level_info(cleaned_code)
        if json_code is None:
            embed = Embed(title="⚙️ Level API Unavailable", color=0xFF0000)
            embed.add_field(name=" ", value="The level API is temporarily unavailable. Please try again later.")
            await ctx.send(embed=embed)
            return

        if "error" in json_code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value=f"Level `{cleaned_code}` is not valid according to the API. Please check the level code and try again.",
            )
            await ctx.send(embed=embed)
            return

        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

        embed = Embed(
            title=f"📷 {json_code.get('name', 'Unknown Level')} ({formatted_code})",
            color=0x2E85FF,
        )
        embed.set_image(
            url=f"https://images.weserv.nl/?url=https://tgrcode.com/mm2/level_entire_thumbnail/{cleaned_code}&output=jpeg"
        )
        await ctx.send(embed=embed)

    # -------------------------
    # GETTING LINK TO LEVEL VIEWER
    # -------------------------
    @commands.command()
    async def viewer(self, ctx, code: str = None, user: User = None):
        if not code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(name=" ", value="Incorrect format. Try `!viewer LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value="Invalid code format. Please use the format `!viewer LEV-ELC-ODE` or `!viewer LEVELCODE`.",
            )
            await ctx.send(embed=embed)
            return

        json_code = self.get_level_info(cleaned_code)
        if json_code is None:
            embed = Embed(title="⚙️ Level API Unavailable", color=0xFF0000)
            embed.add_field(name=" ", value="The level API is temporarily unavailable. Please try again later.")
            await ctx.send(embed=embed)
            return

        if "error" in json_code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value=f"Level `{cleaned_code}` is not valid according to the API. Please check the level code and try again.",
            )
            await ctx.send(embed=embed)
            return

        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

        embed = Embed(
            title=f"🔎 {json_code.get('name', 'Unknown Level')} ({formatted_code})",
            color=0x2E85FF,
        )
        embed.set_thumbnail(
            url=f"https://images.weserv.nl/?url=https://tgrcode.com/mm2/level_thumbnail/{cleaned_code}&output=jpeg"
        )
        embed.add_field(name=" ", value=f"https://smm2.wizul.us/smm2/level/{cleaned_code}")
        await ctx.send(embed=embed)

    # -------------------------
    # GETTING LINK TO LEVEL VIEWER WITHOUT API
    # -------------------------
    @commands.command()
    async def viewersimple(self, ctx, code: str = None, user: User = None):
        if not code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(name=" ", value="Incorrect format. Try `!viewersimple LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Searching Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value="Invalid code format. Please use the format `!viewersimple LEV-ELC-ODE` or `!viewersimple LEVELCODE`.",
            )
            await ctx.send(embed=embed)
            return

        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

        embed = Embed(title=f"🔎 ({formatted_code})", color=0x2E85FF)
        embed.add_field(name=" ", value=f"https://smm2.wizul.us/smm2/level/{cleaned_code}")
        await ctx.send(embed=embed)

    # -------------------------
    # HELPERS
    # -------------------------
    def clean(self, level_code):
        cleaned = re.sub("[^A-Za-z0-9]+", "", level_code).upper()
        return cleaned if len(cleaned) == 9 else None

    def get_level_info(self, level_code):
        url = f"https://tgrcode.com/mm2/level_info/{level_code}"
        try:
            # timeout prevents hanging the entire bot when API is slow/down
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching level info: {e}")
            return None


async def setup(bot):
    await bot.add_cog(ViewerCommands(bot))
