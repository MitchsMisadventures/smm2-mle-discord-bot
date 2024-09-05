from discord.ext import commands
from discord import Embed
import requests, re, discord

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

        cleaned_code = self.clean(code)
        if not cleaned_code:
            embed = Embed(
                title="⚙️ Error Adding Level",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Invalid code format. Please use the format `!add LEV-ELC-ODE` or `!add LEVELCODE`.")
            await ctx.send(embed=embed)
            return

        json_code = self.get_level_info(cleaned_code)

        if not json_code or 'error' in json_code:
            embed = Embed(
                title="⚙️ Error Adding Level",
                color=0xFF0000
            )
            embed.add_field(name=' ', value=f"Level `{cleaned_code}` is not valid according to the API. Please check the level code and try again.")
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

            formatted_code = f"{cleaned_code[0:3]}-{cleaned_code[3:6]}-{cleaned_code[6:9]}"

            embed = Embed(
                title=f"🌴 New Level Added! ({formatted_code})",
                description='---',
                color=self.difficulty_color(json_code['difficulty_name'])
            )
            embed.add_field(name=f'Name', value=f'{json_code['name']}')
            embed.add_field(name='Description', value=json_code['description'], inline=False)
            embed.add_field(name='Style', value=json_code['game_style_name'], inline=False)
            embed.add_field(name='Theme', value=json_code['theme_name'], inline=False)
            embed.add_field(name='Difficulty', value=f"{json_code['difficulty_name']} ({json_code['clear_rate_pretty']})", inline=False)

            embed.set_image(url=f"https://images.weserv.nl/?url=https://tgrcode.com/mm2/level_thumbnail/{cleaned_code}&output=jpeg")

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

        cleaned_code = self.clean(code)
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

    def clean(self, level_code):
        cleaned = re.sub('[^A-Za-z0-9]+', '', level_code).upper()  
        return cleaned if len(cleaned) == 9 else None
    
    def get_level_info(self, level_code):
        url = f'https://tgrcode.com/mm2/level_info/{level_code}'

        try:
            response = requests.get(url)
            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching level info: {e}")
            return None
        
    def difficulty_color(self, value):
        color_val = 0

        if value == 'Easy':
            color_val = 0x7DFFFF
        elif value == 'Normal':
            color_val = 0xA0C78E
        elif value == 'Expert':
            color_val = 0x8A7A4A
        else:
            color_val = 0x674EA7
        return color_val





async def setup(bot):
    await bot.add_cog(LevelCommands(bot))
