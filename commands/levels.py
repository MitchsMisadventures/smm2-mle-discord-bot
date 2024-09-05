from discord.ext import commands
import discord
from discord import Embed
import requests
import re 

class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

### ADDING LEVEL ### 

    @commands.command()
    async def add(self, ctx, code: str = None, user: discord.User = None): 
        if not code:
            embed = Embed(
                title="⚙️ Error Adding Level",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Add a level by providing the Level ID! `!add LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean_and_validate_level_id(code)
        if not cleaned_code:
            embed = Embed(
                title="⚙️ Error Adding Level",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Invalid code format. Please use the format `!add LEV-ELC-ODE` or `!add LEVELCODE`.")
            await ctx.send(embed=embed)
            return

        if not user:
            user = ctx.author 

        async with self.bot.db.cursor() as crs:
            await crs.execute(
                "SELECT 1 FROM Levels WHERE server_id = ? AND level_code = ?",
                (ctx.guild.id, cleaned_code)
            )
            result = await crs.fetchone()

            if result:
                embed = Embed(
                    title="⚙️ Error Adding Level",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"Level `{cleaned_code}` is already registered in this server.")
                await ctx.send(embed=embed)
                return

            await crs.execute(
                "INSERT INTO Levels (server_id, user_id, level_code) VALUES (?, ?, ?)",
                (ctx.guild.id, user.id, cleaned_code)
            )
            await self.bot.db.commit()

            embed = Embed(
                title="🌴 Level Added",
                color=0x00FF00
            )
            embed.add_field(name=' ', value=f"Level `{cleaned_code}` has been submitted by {user.mention}! Thank you!")
            await ctx.send(embed=embed)

### REMOVE LEVEL ### 

    @commands.command()
    async def remove(self, ctx, code: str = None, user: discord.User = None): 
        if not code:
            embed = Embed(
                title="⚙️ Error Removing Level",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Remove a level by providing the Level ID! `!remove LEV-ELC-ODE`")
            await ctx.send(embed=embed)
            return

        cleaned_code = self.clean_and_validate_level_id(code)
        if not cleaned_code:
            embed = Embed(
                title="⚙️ Error Removing Level",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Invalid code format. Please use the format `!remove LEV-ELC-ODE` or `!remove LEVELCODE`.")
            await ctx.send(embed=embed)
            return

        if not user:
            user = ctx.author 

        async with self.bot.db.cursor() as crs:
            await crs.execute(
                "SELECT level_code FROM Levels WHERE server_id = ? AND user_id = ? AND level_code = ?",
                (ctx.guild.id, user.id, cleaned_code)
            )
            result = await crs.fetchone()

            if not result:
                embed = Embed(
                    title="⚙️ Error Removing Level",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"Level `{cleaned_code}` is not registered under your account or does not exist.")
                await ctx.send(embed=embed)
                return

            await crs.execute(
                "DELETE FROM Levels WHERE server_id = ? AND user_id = ? AND level_code = ?",
                (ctx.guild.id, user.id, cleaned_code)
            )
            await self.bot.db.commit()

            embed = Embed(
                title="🍂 Level Removed",
                color=0x00FF00
            )
            embed.add_field(name=' ', value=f"Level `{cleaned_code}` has been removed.")
            await ctx.send(embed=embed)

    def clean_and_validate_level_id(self, level_code):
        cleaned = re.sub('[^A-Za-z0-9]+', '', level_code).upper()  
        return cleaned if len(cleaned) == 9 else None


async def setup(bot):
    await bot.add_cog(LevelCommands(bot))
