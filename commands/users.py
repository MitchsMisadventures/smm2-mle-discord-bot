from discord.ext import commands
from discord import Embed
import re
import aiohttp
import asyncio


API_USER_INFO = "https://tgrcode.com/mm2/user_info/{}"


class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # COMMANDS
    # -------------------------

    @commands.command()
    async def register(self, ctx, code: str = None):
        if not code:
            await ctx.send(embed=self._err("Error Registering User", "Register with your Maker ID: `!register MAK-ERC-ODE`"))
            return

        maker_code = self._normalize_code(code)
        if not maker_code:
            await ctx.send(embed=self._err("Error Registering User", "Invalid code format. Example: `W76-SSW-BTG`"))
            return

        server_id = ctx.guild.id
        user_id = ctx.author.id

        async with self.bot.pg.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO discord_users (server_id, user_id)
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING
                """,
                server_id, user_id,
            )

            await conn.execute(
                """
                INSERT INTO makers (maker_code)
                VALUES ($1)
                ON CONFLICT DO NOTHING
                """,
                maker_code,
            )

            try:
                await conn.execute(
                    """
                    INSERT INTO discord_user_makers (server_id, user_id, maker_code)
                    VALUES ($1, $2, $3)
                    """,
                    server_id, user_id, maker_code,
                )
            except Exception:
                await ctx.send(embed=self._err(
                    "Error Registering User",
                    "You are already registered, or that Maker ID is already claimed in this server.",
                ))
                return

        # Respond immediately (no friction)
        formatted = self._format_code(maker_code)
        embed = Embed(title="🌱 Maker Registered", color=0x00FF00)
        embed.add_field(name=" ", value=f"Registered Maker ID **{formatted}** to {ctx.author.mention}")
        await ctx.send(embed=embed)

        # Best-effort background sync (doesn't block the command)
        asyncio.create_task(self._sync_maker_by_code(maker_code))

    @commands.command()
    async def myid(self, ctx):
        row = await self.bot.pg.fetchrow(
            """
            SELECT maker_code
            FROM discord_user_makers
            WHERE server_id = $1 AND user_id = $2
            """,
            ctx.guild.id, ctx.author.id,
        )

        if not row:
            await ctx.send(embed=self._err("Error Retrieving Maker ID", "No Maker ID found for this user."))
            return

        maker_code = row["maker_code"]
        embed = Embed(title="Your Maker ID", color=0x00FF00)
        embed.add_field(name=" ", value=f"{ctx.author.mention}, your Maker ID is: `{self._format_code(maker_code)}`")
        await ctx.send(embed=embed)

    @commands.command()
    async def unregister(self, ctx):
        result = await self.bot.pg.execute(
            """
            DELETE FROM discord_user_makers
            WHERE server_id = $1 AND user_id = $2
            """,
            ctx.guild.id, ctx.author.id,
        )

        if result.endswith("0"):
            await ctx.send(embed=self._err("Error Unregistering User", "You are not registered."))
            return

        embed = Embed(title="🍃 User Unregistered", color=0x00FF00)
        embed.add_field(name=" ", value=f"{ctx.author.mention} has unregistered their Maker ID.")
        await ctx.send(embed=embed)

    # Optional manual retry tool (keep it, but users don't need it)
    @commands.command()
    async def sync(self, ctx):
        row = await self.bot.pg.fetchrow(
            """
            SELECT maker_code
            FROM discord_user_makers
            WHERE server_id = $1 AND user_id = $2
            """,
            ctx.guild.id, ctx.author.id,
        )

        if not row:
            await ctx.send(embed=self._err("Sync Failed", "You are not registered."))
            return

        ok = await self._sync_maker_by_code(row["maker_code"])
        if not ok:
            await ctx.send(embed=self._err("Sync Failed", "Could not fetch maker data. Try again later."))
            return

        embed = Embed(title="🌱 Maker Synced", color=0x00FF00)
        embed.add_field(name=" ", value="Your maker profile has been updated.")
        await ctx.send(embed=embed)

    # -------------------------
    # INTERNALS (1 job each)
    # -------------------------

    async def _sync_maker_by_code(self, maker_code: str) -> bool:
        """Fetch maker info from API and upsert into DB. Returns True on success."""
        payload = await self._fetch_maker_info(maker_code)
        if not payload:
            return False

        async with self.bot.pg.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO makers (
                    maker_code,
                    pid,
                    maker_name,
                    country,
                    region_name,
                    mii_image,
                    updated_at
                )
                VALUES ($1,$2,$3,$4,$5,$6, NOW())
                ON CONFLICT (maker_code) DO UPDATE SET
                    pid = EXCLUDED.pid,
                    maker_name = EXCLUDED.maker_name,
                    country = EXCLUDED.country,
                    region_name = EXCLUDED.region_name,
                    mii_image = EXCLUDED.mii_image,
                    updated_at = NOW()
                """,
                payload.get("code"),
                payload.get("pid"),
                payload.get("name"),
                payload.get("country"),
                payload.get("region_name"),
                payload.get("mii_image"),
            )

        return True

    async def _fetch_maker_info(self, maker_code: str):
        url = API_USER_INFO.format(maker_code)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except Exception as e:
            print(f"[users] Error fetching maker info for {maker_code}: {e}")
            return None

    # -------------------------
    # SMALL HELPERS (pure)
    # -------------------------

    def _normalize_code(self, code: str):
        cleaned = re.sub("[^A-Za-z0-9]+", "", code).upper()
        return cleaned if len(cleaned) == 9 else None

    def _format_code(self, code: str) -> str:
        return f"{code[0:3]}-{code[3:6]}-{code[6:9]}"

    def _err(self, title: str, msg: str) -> Embed:
        embed = Embed(title=f"⚙️ {title}", color=0xFF0000)
        embed.add_field(name=" ", value=msg)
        return embed


async def setup(bot):
    await bot.add_cog(UserCommands(bot))
