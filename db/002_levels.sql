-- db/002_levels.sql
BEGIN;

CREATE TABLE IF NOT EXISTS levels (
  server_id   BIGINT NOT NULL,
  level_code  TEXT NOT NULL, -- normalized, no dashes (9 chars)
  added_by_user_id BIGINT NOT NULL, -- discord user id (who added it)

  level_name  TEXT,
  theme       TEXT,
  style       TEXT,
  difficulty  TEXT,
  clear_video TEXT,

  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  PRIMARY KEY (server_id, level_code),

  -- Ensure "added_by_user_id" exists as a discord user in that server
  FOREIGN KEY (server_id, added_by_user_id)
    REFERENCES discord_users(server_id, user_id)
    ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_levels_added_by
  ON levels (server_id, added_by_user_id);

COMMIT;
