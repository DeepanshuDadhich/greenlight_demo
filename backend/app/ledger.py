import json
from datetime import datetime, timezone
from typing import Any

import aiosqlite

_SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ledger_run_id ON ledger_entries(run_id);
"""


class Ledger:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.executescript(_SCHEMA)
            await db.commit()

    async def record(self, run_id: str, event_type: str, payload: dict[str, Any]) -> None:
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO ledger_entries (run_id, event_type, payload, created_at) VALUES (?, ?, ?, ?)",
                (run_id, event_type, json.dumps(payload), datetime.now(timezone.utc).isoformat()),
            )
            await db.commit()

    async def history(self, run_id: str) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT event_type, payload, created_at FROM ledger_entries WHERE run_id = ? ORDER BY id ASC",
                (run_id,),
            )
            rows = await cursor.fetchall()
            return [
                {
                    "event_type": row["event_type"],
                    "payload": json.loads(row["payload"]),
                    "created_at": row["created_at"],
                }
                for row in rows
            ]
