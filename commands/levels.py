from discord.ext import commands
from discord import Embed, User
import aiohttp
import re


API_LEVEL_INFO = "https://tgrcode.com/mm2/level_info/{}"


class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # ADD LEVEL
    # -------------------------

    @commands.command()
    async def add(self, ctx, code: str = None, user: User = None):

        if not code:
            embed = Embed(title="⚙️ Error Adding Level", color=0xFF0000)
            embed.add_field(name=" ", value="Add a level by providing the Level ID! `!add LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Adding Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value="Invalid code format. Please use the format `!add LEV-ELC-ODE` or `!add LEVELCODE`.",
            )
            await ctx.send(embed=embed)
            return

        json_code = await self.get_level_info(cleaned_code)
        if not json_code or "error" in json_code:
            embed = Embed(title="⚙️ Error Adding Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value=f"Level `{cleaned_code}` is not valid according to the API. Please check the level code and try again.",
            )
            await ctx.send(embed=embed)
            return

        if not user:
            user = ctx.author

        server_id = ctx.guild.id if ctx.guild else 0

        # Check for duplicate level in this server
        exists = await self.bot.pg.fetchrow(
            "SELECT 1 FROM levels WHERE server_id = $1 AND level_code = $2",
            server_id,
            cleaned_code,
        )

        if exists:
            embed = Embed(title="⚙️ Error Adding Level", color=0xFF0000)
            embed.add_field(name=" ", value=f"Level `{cleaned_code}` is already registered in this server.")
            await ctx.send(embed=embed)
            return

        await self.bot.pg.execute(
            """
            INSERT INTO levels (
                server_id,
                added_by_user_id,
                level_code,
                level_name,
                theme,
                style,
                difficulty
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            server_id,
            user.id,
            cleaned_code,
            json_code.get("name"),
            json_code.get("theme_name"),
            json_code.get("game_style_name"),
            json_code.get("difficulty_name"),
        )

        # -------- Embed formatting --------

        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"
        uploader = json_code.get("uploader") or {}
        uploader_code = uploader.get("code", "?????????")
        formatted_maker = (
            f"{uploader_code[0:3]}-{uploader_code[3:6]}-{uploader_code[6:9]}"
            if len(uploader_code) == 9
            else uploader_code
        )

        embed = Embed(
            title=f"🌴 New Level Added! ({formatted_code})",
            description="---",
            color=self.difficulty_color(json_code.get("difficulty_name")),
        )

        embed.add_field(
            name=json_code.get("name", "Unknown Level"),
            value=json_code.get("description", "No description provided."),
            inline=False,
        )
        embed.add_field(name="Style", value=json_code.get("game_style_name", "Unknown"), inline=False)
        embed.add_field(name="Theme", value=json_code.get("theme_name", "Unknown"), inline=False)
        embed.add_field(
            name="Difficulty",
            value=f"{json_code.get('difficulty_name')} (**{json_code.get('clear_rate_pretty', 'N/A')}**)",
            inline=False,
        )
        embed.add_field(
            name="Uploaded By",
            value=f"{uploader.get('name', 'Unknown')} (**{formatted_maker}**)",
            inline=False,
        )

        embed.set_thumbnail(url=uploader.get("mii_image"))
        embed.set_image(
            url=f"https://images.weserv.nl/?url=https://tgrcode.com/mm2/level_thumbnail/{cleaned_code}&output=jpeg"
        )

        await ctx.send(embed=embed)

    # -------------------------
    # REMOVE LEVEL
    # -------------------------

    @commands.command()
    async def remove(self, ctx, code: str = None, user: User = None):
        if not code:
            embed = Embed(title="⚙️ Error Removing Level", color=0xFF0000)
            embed.add_field(name=" ", value="Remove a level by providing the Level ID! `!remove LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Removing Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value="Invalid code format. Please use the format `!remove LEV-ELC-ODE` or `!remove LEVELCODE`.",
            )
            await ctx.send(embed=embed)
            return

        if not user:
            user = ctx.author

        server_id = ctx.guild.id if ctx.guild else 0

        row = await self.bot.pg.fetchrow(
            """
            SELECT level_code, level_name
            FROM levels
            WHERE server_id = $1 AND added_by_user_id = $2 AND level_code = $3
            """,
            server_id,
            user.id,
            cleaned_code,
        )

        if not row:
            embed = Embed(title="⚙️ Error Removing Level", color=0xFF0000)
            embed.add_field(
                name=" ",
                value=f"Level `{cleaned_code}` is not registered under your account or does not exist.",
            )
            await ctx.send(embed=embed)
            return

        await self.bot.pg.execute(
            "DELETE FROM levels WHERE server_id = $1 AND added_by_user_id = $2 AND level_code = $3",
            server_id,
            user.id,
            cleaned_code,
        )

        embed = Embed(
            title=f"🍂 Level Removed ({cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]})",
            description="---",
            color=0x00FF00,
        )
        embed.add_field(name=" ", value=f"**{row['level_name']}** has been removed from the database.")
        await ctx.send(embed=embed)

    # -------------------------
    # HELPERS
    # -------------------------

    def clean(self, level_code: str):
        cleaned = re.sub("[^A-Za-z0-9]+", "", level_code).upper()
        return cleaned if len(cleaned) == 9 else None

    async def get_level_info(self, level_code: str):
        url = API_LEVEL_INFO.format(level_code)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except Exception as e:
            print(f"[levels] Error fetching level info for {level_code}: {e}")
            return None

    def difficulty_color(self, value: str):
        if value == "Easy":
            return 0x7DFFFF
        elif value == "Normal":
            return 0xA0C78E
        elif value == "Expert":
            return 0x8A7A4A
        else:
            return 0x674EA7


async def setup(bot):
    await bot.add_cog(LevelCommands(bot))
