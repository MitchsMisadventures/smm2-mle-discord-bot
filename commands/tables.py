from discord import Embed, User
from discord.ext import commands
import re


class TableCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # GETTING ALL USER LEVELS FROM SERVER
    # -------------------------
    @commands.command()
    async def mylevels(self, ctx, user: User = None):
        guild_id = ctx.guild.id if ctx.guild else 0

        if not user:
            user = ctx.author

        levels = await self.bot.pg.fetch(
            """
            SELECT level_code, level_name
            FROM levels
            WHERE user_id = $1 AND server_id = $2
            ORDER BY created_at DESC
            """,
            user.id,
            guild_id,
        )

        if levels:
            embed = Embed(
                title=f"✨ {user.display_name}'s Levels ✨",
                description="---",
                color=0x808080,
            )

            for row in levels:
                level_code = row["level_code"]
                level_name = row["level_name"] or "Untitled Level"
                formatted_code = f"{level_code[0:3]}-{level_code[3:6]}-{level_code[6:9]}"
                embed.add_field(name=level_name, value=f"`{formatted_code}`", inline=False)

            await ctx.send(embed=embed)
        else:
            embed = Embed(title="⚙️ Error Retrieving Levels", color=0xFFFF00)
            embed.add_field(name=" ", value="No levels found for this user.")
            await ctx.send(embed=embed)

    # -------------------------
    # GETTING RANDOM LEVEL FROM SERVER
    # -------------------------
    @commands.command()
    async def random(self, ctx):
        guild_id = ctx.guild.id if ctx.guild else 0

        row = await self.bot.pg.fetchrow(
            """
            SELECT level_code, level_name
            FROM levels
            WHERE server_id = $1
            ORDER BY RANDOM()
            LIMIT 1
            """,
            guild_id,
        )

        if row:
            level_code = row["level_code"]
            level_name = row["level_name"] or "Untitled Level"
            formatted_code = f"{level_code[0:3]}-{level_code[3:6]}-{level_code[6:9]}"

            embed = Embed(title=f"🎲 {level_name} ({formatted_code})", color=0x808080)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title="⚙️ Error Retrieving Levels", color=0xFFFF00)
            embed.add_field(
                name=" ",
                value="No levels found in this server. Consider adding one with `!add LEV-ELC-ODE`",
            )
            await ctx.send(embed=embed)

    # -------------------------
    # GETTING SERVER LEVEL COUNT
    # -------------------------
    @commands.command()
    async def levelcount(self, ctx):
        guild_id = ctx.guild.id if ctx.guild else 0

        row = await self.bot.pg.fetchrow(
            "SELECT COUNT(*) AS cnt FROM levels WHERE server_id = $1",
            guild_id,
        )

        count = row["cnt"] if row else 0

        embed = Embed(title=f"There are **{count}** levels in this server!", color=0x808080)
        await ctx.send(embed=embed)

    def clean(self, level_code):
        cleaned = re.sub("[^A-Za-z0-9]+", "", level_code).upper()
        return cleaned if len(cleaned) == 9 else None


async def setup(bot):
    await bot.add_cog(TableCommands(bot))
