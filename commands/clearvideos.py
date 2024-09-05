from discord.ext import commands
import discord
from discord import Embed
import re 

class ClearVidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

### ADDING CLEAR VIDEO ### 

    @commands.command()
    async def addclearvid(self, ctx, code: str = None, clearvid: str = None, user: discord.User = None):
        if not code:
            embed = Embed(
                title="⚙️ Error Adding Clear Video",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Please provide the Level ID. Example: `!addclearvid LEVELCODE youtube.com`")
            await ctx.send(embed=embed)
            return

        if not clearvid:
            embed = Embed(
                title="⚙️ Error Adding Clear Video",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Please provide the clear video URL. Example: `!addclearvid LEVELCODE youtube.com`")
            await ctx.send(embed=embed)
            return

        async with self.bot.db.cursor() as crs:
            await crs.execute("SELECT level_code FROM Levels WHERE level_code = ?", (code,))
            level_exists = await crs.fetchone()

            if not level_exists:
                embed = Embed(
                    title="⚙️ Level Not Found",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"Level `{code}` does not exist in the database.")
                await ctx.send(embed=embed)
                return

            await crs.execute(
                "UPDATE Levels SET clear_video = ? WHERE level_code = ?",
                (clearvid, code)
            )
            await self.bot.db.commit()

        embed = Embed(
            title="🎥 Clear Video Added",
            color=0x00FF00
        )
        embed.add_field(name=' ', value=f"Clear video for Level `{code}` has been added: {clearvid}")
        await ctx.send(embed=embed)

### SHOWING CLEAR VID ### 

    @commands.command()
    async def clearvid(self, ctx, code: str = None, user: discord.User = None):
        if not code:
            embed = Embed(
                title="⚙️ Error Retrieving Clear Video",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Please provide the Level ID. Example: `!clearvid LEVELCODE`")
            await ctx.send(embed=embed)
            return

        async with self.bot.db.cursor() as crs:
            await crs.execute("SELECT clear_video FROM Levels WHERE level_code = ?", (code,))
            result = await crs.fetchone()

        if not result or not result[0]:
            embed = Embed(
                title="⚙️ Clear Video Not Found",
                color=0xFF0000
            )
            embed.add_field(name=' ', value=f"No clear video found for Level `{code}`. It may not exist or hasn't been set.")
            await ctx.send(embed=embed)
            return

        clearvid_url = result[0]

        embed = Embed(
            title="🎥 Clear Video Found",
            color=0x00FF00
        )
        embed.add_field(name=' ', value=f"Clear video for Level `{code}`:")
        
        await ctx.send(embed=embed)
        await ctx.send(clearvid_url)

### REMOVING CLEAR VIDEO ### 

    @commands.command()
    async def removeclearvid(self, ctx, code: str = None):
        if not code:
            embed = Embed(
                title="⚙️ Error Removing Clear Video",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Please provide the Level ID. Example: `!removeclearvid LEVELCODE`")
            await ctx.send(embed=embed)
            return

        async with self.bot.db.cursor() as crs:
            await crs.execute(
                "SELECT user_id, clear_video FROM Levels WHERE level_code = ?",
                (code,)
            )
            result = await crs.fetchone()

            if not result:
                embed = Embed(
                    title="⚙️ Clear Video Not Found",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"No clear video found for Level `{code}` or level does not exist.")
                await ctx.send(embed=embed)
                return

            user_id, clearvid_url = result

            if clearvid_url is None:
                embed = Embed(
                    title="⚙️ Clear Video Not Found",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"No clear video found for Level `{code}`. It may not exist or hasn't been set.")
                await ctx.send(embed=embed)
                return

            if user_id != ctx.author.id:
                embed = Embed(
                    title="⚙️ Error Removing Clear Video",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value="You can only remove clear videos that you have added.")
                await ctx.send(embed=embed)
                return

            await crs.execute(
                "UPDATE Levels SET clear_video = NULL WHERE level_code = ?",
                (code,)
            )
            await self.bot.db.commit()

            embed = Embed(
                title="💨 Clear Video Removed",
                color=0x00FF00
            )
            embed.add_field(name=' ', value=f"Clear video for Level `{code}` has been removed.")
            await ctx.send(embed=embed)

    def clean_and_validate_level_id(self, level_code):
        cleaned = re.sub('[^A-Za-z0-9]+', '', level_code).upper()  
        return cleaned if len(cleaned) == 9 else None


async def setup(bot):
    await bot.add_cog(ClearVidCommands(bot))
