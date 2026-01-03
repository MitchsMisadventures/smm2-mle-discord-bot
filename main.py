import os
import asyncio
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

from db import create_pool, init_schema

EXTENSIONS = [
    "commands.levels",
    "commands.credits",
    "commands.users",
    "commands.clearvideos",
    "commands.helpc",
    "commands.tables",
    "commands.viewer",
]

class LevelExchangeBot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        self.remove_command("help")
        self.pg = None  # asyncpg pool

    async def setup_hook(self) -> None:

        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL is not set.")

        self.pg = await create_pool(database_url)
        await init_schema(self.pg)

        for ext in EXTENSIONS:
            try:
                await self.load_extension(ext)
            except Exception as e:
                print(f"Failed to load {ext}: {e}")
                raise  

    async def close(self) -> None:
        try:
            if self.pg:
                await self.pg.close()
        finally:
            await super().close()

bot = LevelExchangeBot()

@bot.event
async def on_ready():
    print("Bot is running . . .")
    print(f"Logged in as {bot.user} (id: {bot.user.id})")

async def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set.")

    await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())
