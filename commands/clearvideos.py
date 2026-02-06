from discord.ext import commands
import discord
from discord import Embed
import re
import aiohttp

class ClearVidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # ADDING CLEAR VIDEO
    # -------------------------
    @commands.command()
    async def addclearvid(self, ctx, code: str = None, clearvid: str = None, user: discord.User = None):
        if not code:
            embed = Embed(title="⚙️ Error Adding Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Please provide the Level ID. Example: `!addclearvid LEVELCODE youtube.com`")
            await ctx.send(embed=embed)
            return

        if not clearvid:
            embed = Embed(title="⚙️ Error Adding Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Please provide the clear video URL. Example: `!addclearvid LEVELCODE youtube.com`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Adding Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Invalid Level ID format.")
            await ctx.send(embed=embed)
            return

        server_id = ctx.guild.id if ctx.guild else 0
        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

        row = await self.bot.pg.fetchrow(
            """
            SELECT level_code, clear_video
            FROM levels
            WHERE server_id = $1 AND level_code = $2
            """,
            server_id,
            cleaned_code,
        )

        if not row:
            embed = Embed(title="⚙️ Level Not Found", color=0xFF0000)
            embed.add_field(name=" ", value=f"Level `{formatted_code}` does not exist in the database.")
            await ctx.send(embed=embed)
            return

        if row["clear_video"]:
            embed = Embed(title="⚙️ Clear Video Already Exists", color=0xFF0000)
            embed.add_field(name=" ", value=f"A clear video already exists for `{formatted_code}`.")
            await ctx.send(embed=embed)
            return

        await self.bot.pg.execute(
            """
            UPDATE levels
            SET clear_video = $1
            WHERE server_id = $2 AND level_code = $3
            """,
            clearvid,
            server_id,
            cleaned_code,
        )

        embed = Embed(title="🎥 Clear Video Added", color=0x00FF00)
        embed.add_field(name=" ", value=f"Clear video for `{formatted_code}` has been added: {clearvid}")
        await ctx.send(embed=embed)

    # -------------------------
    # SHOWING CLEAR VID
    # -------------------------
    @commands.command()
    async def clearvid(self, ctx, code: str = None, user: discord.User = None):
        if not code:
            embed = Embed(title="⚙️ Error Retrieving Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Please provide the Level ID. Example: `!clearvid LEVELCODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Retrieving Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Invalid Level ID format.")
            await ctx.send(embed=embed)
            return

        server_id = ctx.guild.id if ctx.guild else 0
        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

        row = await self.bot.pg.fetchrow(
            """
            SELECT clear_video
            FROM levels
            WHERE server_id = $1 AND level_code = $2
            """,
            server_id,
            cleaned_code,
        )

        if not row or not row["clear_video"]:
            embed = Embed(title="⚙️ Clear Video Not Found", color=0xFF0000)
            embed.add_field(
                name=" ",
                value=f"No clear video found for `{formatted_code}`. It may not exist or hasn't been set.",
            )
            await ctx.send(embed=embed)
            return

        clearvid_url = row["clear_video"]

        embed = Embed(title="🎥 Clear Video Found", color=0x00FF00)
        embed.add_field(name=" ", value=f"Clear video for `{formatted_code}`:")
        await ctx.send(embed=embed)
        await ctx.send(clearvid_url)

    # -------------------------
    # REMOVING CLEAR VIDEO
    # -------------------------
    @commands.command()
    async def removeclearvid(self, ctx, code: str = None):
        if not code:
            embed = Embed(title="⚙️ Error Removing Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Please provide the Level ID. Example: `!removeclearvid LEVELCODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(title="⚙️ Error Removing Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="Invalid Level ID format.")
            await ctx.send(embed=embed)
            return

        server_id = ctx.guild.id if ctx.guild else 0
        formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

        row = await self.bot.pg.fetchrow(
            """
            SELECT user_id, clear_video
            FROM levels
            WHERE server_id = $1 AND level_code = $2
            """,
            server_id,
            cleaned_code,
        )

        if not row or row["clear_video"] is None:
            embed = Embed(title="⚙️ Clear Video Not Found", color=0xFF0000)
            embed.add_field(
                name=" ",
                value=f"No clear video found for `{formatted_code}` or level does not exist.",
            )
            await ctx.send(embed=embed)
            return

        if row["user_id"] != ctx.author.id:
            embed = Embed(title="⚙️ Error Removing Clear Video", color=0xFF0000)
            embed.add_field(name=" ", value="You can only remove clear videos that you have added.")
            await ctx.send(embed=embed)
            return

        await self.bot.pg.execute(
            """
            UPDATE levels
            SET clear_video = NULL
            WHERE server_id = $1 AND level_code = $2
            """,
            server_id,
            cleaned_code,
        )

        embed = Embed(title="💨 Clear Video Removed", color=0x00FF00)
        embed.add_field(name=" ", value=f"Clear video for `{formatted_code}` has been removed.")
        await ctx.send(embed=embed)

    def clean(self, level_code):
        cleaned = re.sub("[^A-Za-z0-9]+", "", level_code).upper()
        return cleaned if len(cleaned) == 9 else None


async def setup(bot):
    await bot.add_cog(ClearVidCommands(bot))
