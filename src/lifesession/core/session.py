"""Session lifecycle — demo/simulation only. No production execution."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Session:
    session_type: str
    owner: str
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
    status: str = "open"

    def close(self, summary: str = "") -> dict:
        self.closed_at = datetime.now(timezone.utc)
        self.status = "closed"
        return {
            "session_id": self.session_id,
            "closed_at": self.closed_at.isoformat(),
            "summary": summary,
        }
