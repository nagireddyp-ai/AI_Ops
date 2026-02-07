from datetime import datetime

from pydantic import BaseModel


class LogEntry(BaseModel):
    id: str
    incident_id: str
    level: str
    message: str
    timestamp: datetime
