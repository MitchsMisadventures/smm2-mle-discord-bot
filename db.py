import asyncpg

async def create_pool(dsn: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=1,
        max_size=5,
        command_timeout=30,
    )

async def init_schema(pool: asyncpg.Pool) -> None:
    """
    Mirrors your existing SQLite schema intent, but with:
    - BIGINT for Discord IDs
    - primary keys to prevent duplicates
    - indexes for common lookups
    """
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            server_id  BIGINT NOT NULL,
            user_id    BIGINT NOT NULL,
            maker_id   TEXT   NOT NULL,
            clears     INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            PRIMARY KEY (server_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS levels (
            server_id   BIGINT NOT NULL,
            level_code  TEXT   NOT NULL,
            user_id     BIGINT NOT NULL,
            level_name  TEXT,
            theme       TEXT,
            style       TEXT,
            difficulty  TEXT,
            rating      INTEGER,
            clear_video TEXT,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            PRIMARY KEY (server_id, level_code)
        );

        CREATE INDEX IF NOT EXISTS idx_levels_server_user
            ON levels(server_id, user_id);

        CREATE INDEX IF NOT EXISTS idx_levels_server
            ON levels(server_id);

        """)
