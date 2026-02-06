BEGIN;

-- 1) Discord users (per server)
CREATE TABLE IF NOT EXISTS discord_users (
  server_id  BIGINT NOT NULL,
  user_id    BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (server_id, user_id)
);

-- 2) SMM2 makers (global dimension)
CREATE TABLE IF NOT EXISTS makers (
  maker_code  TEXT PRIMARY KEY,   -- normalized, no dashes (e.g., W76SSWBTG)
  pid         BIGINT,
  maker_name  TEXT,
  country     TEXT,
  region_name TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3) Link discord user <-> maker (per server)
-- Enforces: one maker per discord user per server
-- Also enforces: one discord user can claim a maker per server (anti-impersonation)
CREATE TABLE IF NOT EXISTS discord_user_makers (
  server_id  BIGINT NOT NULL,
  user_id    BIGINT NOT NULL,
  maker_code TEXT NOT NULL REFERENCES makers(maker_code) ON DELETE RESTRICT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (server_id, user_id),
  UNIQUE (server_id, maker_code)
);

-- Helpful indexes (optional but good)
CREATE INDEX IF NOT EXISTS idx_discord_user_makers_maker
  ON discord_user_makers (maker_code);

COMMIT;