import asyncio, aiosqlite
from discord import Intents
from discord.ext import commands
from creds import *  

intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    bot.db = await aiosqlite.connect('LevelStorage.db')

    crs = await bot.db.cursor()
    await crs.execute("CREATE TABLE IF NOT EXISTS Levels(server_id INTEGER, user_id INTEGER, level_code STR, level_name STR, theme STR, style STR, difficulty STR, rating INTEGER, clear_video STR)") 
    await crs.execute("CREATE TABLE IF NOT EXISTS Users(server_id INTEGER, user_id INTEGER, maker_id STR, clears INTEGER)")
    await bot.db.commit()
    print('Bot is running . . .')

async def load_cogs():
    try:
        await bot.load_extension('commands.levels')
        await bot.load_extension('commands.credits')
        await bot.load_extension('commands.users')
        await bot.load_extension('commands.clearvideos')
        await bot.load_extension('commands.helpc')

    except Exception as e:
        print(f'Failed to load cogs: {e}')
async def main():
    await load_cogs() 
    await bot.start(BOT_TOKEN)  

if __name__ == '__main__':
    asyncio.run(main()) 
