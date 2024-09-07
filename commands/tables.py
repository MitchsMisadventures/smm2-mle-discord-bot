from discord import Embed, User
from discord.ext import commands
import re

class TableCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

### GETTING ALL USER LEVELS FROM SERVER ###

    @commands.command()
    async def mylevels(self, ctx, user: User = None):
        guild_id = ctx.guild.id  

        if not user:
            user = ctx.author 

        async with self.bot.db.cursor() as crs:
            await crs.execute(
                "SELECT level_code, level_name FROM Levels WHERE user_id = ? AND server_id = ?", (user.id, guild_id)
            )
            levels = await crs.fetchall()

            if levels:
                embed = Embed(
                    title=f"✨ {user.display_name}'s Levels ✨",
                    description="---",
                    color=0x808080
                )

                for level_code, level_name in levels:
                    formatted_code = f"{level_code[0:3]}-{level_code[3:6]}-{level_code[6:9]}"
                    embed.add_field(name=level_name, value=f"`{formatted_code}`", inline = False)

                await ctx.send(embed=embed)
            else:
                embed = Embed(
                    title="⚙️ Error Retrieving Levels",
                    color=0xFFFF00
                )
                embed.add_field(name=' ', value="No levels found for this user.")
                await ctx.send(embed=embed)

    def clean(self, level_code):
        cleaned = re.sub('[^A-Za-z0-9]+', '', level_code).upper()  
        return cleaned if len(cleaned) == 9 else None
    
### GETTING RANDOM LEVEL FROM SERVER ###
    
    @commands.command()
    async def random(self, ctx):
        guild_id = ctx.guild.id  

        async with self.bot.db.cursor() as crs:
            await crs.execute(
                "SELECT level_code, level_name FROM Levels WHERE server_id = ? ORDER BY RANDOM() LIMIT 1",
                (guild_id,)
            )
            random_level = await crs.fetchone()

            if random_level:
                level_code, level_name = random_level

                formatted_code = f"{level_code[0:3]}-{level_code[3:6]}-{level_code[6:9]}"

                embed = Embed(
                    title=f"🎲 {level_name} ({formatted_code})",
                    color=0x808080
                )
                await ctx.send(embed=embed)
            else:
                embed = Embed(
                    title="⚙️ Error Retrieving Levels",
                    color=0xFFFF00
                )
                embed.add_field(name=' ', value="No levels found in this server. Consider adding one with `!add LEV-ELC-ODE`")
                await ctx.send(embed=embed)

### GETTING SERVER LEVEL COUNT ###

    @commands.command()
    async def levelcount(self, ctx):
        guild_id = ctx.guild.id  

        async with self.bot.db.cursor() as crs:
            await crs.execute(
                "SELECT COUNT(*) FROM Levels WHERE server_id = ?",
                (guild_id,)
            )
            count_result = await crs.fetchone()

            if count_result:
                count = count_result[0]

                embed = Embed(
                    title=f"There are **{count}** levels in this server!",
                    color=0x808080
                )

                await ctx.send(embed=embed)
            else:
                embed = Embed(
                    title="⚙️ Error Retrieving Levels Count",
                    color=0xFFFF00
                )
                embed.add_field(name=' ', value="Could not retrieve the count of levels.")
                await ctx.send(embed=embed)

    def clean(self, level_code):
        cleaned = re.sub('[^A-Za-z0-9]+', '', level_code).upper()  
        return cleaned if len(cleaned) == 9 else None
    
async def setup(bot):
    await bot.add_cog(TableCommands(bot))
