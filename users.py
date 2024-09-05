from discord.ext import commands
import discord
from discord import Embed

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

### USER REGISTRATION ### 

    @commands.command()
    async def register(self, ctx, code: str = None, user: discord.User = None): 
        if not code:
            embed = Embed(
                title="⚙️ Error Registering User",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Register by adding your Maker ID! `!register MAK-ERC-ODE`")
            await ctx.send(embed=embed)
            return

        if not self.validate_code_format(code):
            embed = Embed(
                title="⚙️ Error Registering User",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Invalid code format. Please use the format `!register MAK-ERC-ODE`.")
            await ctx.send(embed=embed)
            return

        if not user:
            user = ctx.author 

        async with self.bot.db.cursor() as crs:
            await crs.execute("SELECT user_id FROM Users WHERE user_id = ?", (user.id,))
            re = await crs.fetchone()

            if re:
                embed = Embed(
                    title="⚙️ Error Registering User",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"{user.mention}, You already have a Maker ID registered! Try doing `!myid`.")
                await ctx.send(embed=embed)
                return

            await crs.execute("INSERT INTO Users(user_id, maker_id) VALUES(?, ?)", (user.id, code))
            await self.bot.db.commit()

        embed = Embed(
            title="🌱 New User Registered",
            color=0x00FF00
        )
        embed.add_field(name=' ', value=f"Maker code `{code}` has been registered to {user.mention}! Thank you!")
        await ctx.send(embed=embed)

### UNREGISTER USER ### 

    @commands.command()
    async def unregister(self, ctx, code: str = None, user: discord.User = None): 
        if not code:
            embed = Embed(
                title="⚙️ Error Unregistering User",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Unregister by adding your Maker ID, `!unregister MAK-ERC-ODE`")
            await ctx.send(embed=embed)
            return

        if not self.validate_code_format(code):
            embed = Embed(
                title="⚙️ Error Unregistering User",
                color=0xFF0000
            )
            embed.add_field(name=' ', value="Invalid code format. Please use the format `!unregister MAK-ERC-ODE`.")
            await ctx.send(embed=embed)
            return

        if not user:
            user = ctx.author 

        async with self.bot.db.cursor() as crs:
            await crs.execute("SELECT maker_id FROM Users WHERE user_id = ? AND maker_id = ?", (user.id, code))
            re = await crs.fetchone()

            if not re:
                embed = Embed(
                    title="⚙️ Error Unregistering User",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value=f"Maker ID `{code}` is not registered.")
                await ctx.send(embed=embed)
                return

            await crs.execute("DELETE FROM Users WHERE user_id = ? AND maker_id = ?", (user.id, code))
            await self.bot.db.commit()

        embed = Embed(
            title="🍃 User Unregistered",
            color=0x00FF00
        )
        embed.add_field(name=' ', value=f"{user.mention} has unregistered Maker ID, `{code}`. We hope to see you again :)")
        await ctx.send(embed=embed)

### GETTING USER ID ### 

    @commands.command()
    async def myid(self, ctx, user: discord.User = None):
        if not user:
            user = ctx.author

        async with self.bot.db.cursor() as crs:
            await crs.execute("SELECT maker_id FROM Users WHERE user_id = ?", (user.id,))
            re = await crs.fetchone()

            if re:
                maker_id = re[0]
                embed = Embed(
                    title="Your Maker ID",
                    color=0x00FF00
                )
                embed.add_field(name=' ', value=f"{user.mention}, your Maker ID is: `{maker_id}`")
                await ctx.send(embed=embed)
            else:
                embed = Embed(
                    title="⚙️ Error Retrieving Maker ID",
                    color=0xFF0000
                )
                embed.add_field(name=' ', value="No Maker ID found for this user.")
                await ctx.send(embed=embed)

    def validate_code_format(self, code):
        parts = code.split('-')
        return len(parts) == 3 and all(len(part) == 3 for part in parts)

async def setup(bot):
    await bot.add_cog(UserCommands(bot))
