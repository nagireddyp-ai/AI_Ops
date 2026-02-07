import random
from datetime import datetime
from uuid import uuid4

from app.models.incident import Incident
from app.models.log import LogEntry

INCIDENT_TYPES = [
    "Linux server down",
    "Disk full",
    "CPU spike",
    "Network unreachable",
    "Service crash",
    "Patch failure",
    "Security alert",
]

REGIONS = ["us-east-1", "us-west-2", "eu-west-1", "ap-south-1"]
ENVIRONMENTS = ["prod", "dev"]
SEVERITIES = ["P1", "P2", "P3", "P4"]
ENGINEERS = ["Alex Morgan", "Priya Desai", "Chen Wu", "Maria Gomez"]


def generate_hostname(service: str) -> str:
    return f"{service}-{random.randint(1, 120):02d}"


def generate_incident() -> Incident:
    incident_type = random.choice(INCIDENT_TYPES)
    severity = random.choices(SEVERITIES, weights=[10, 25, 35, 30])[0]
    now = datetime.utcnow()
    hostname = generate_hostname("srv")
    return Incident(
        id=str(uuid4()),
        title=f"{incident_type} detected on {hostname}",
        type=incident_type,
        hostname=hostname,
        region=random.choice(REGIONS),
        environment=random.choice(ENVIRONMENTS),
        severity=severity,
        status="new",
        assigned_engineer=random.choice(ENGINEERS),
        escalation_path=["NOC", "SRE", "Incident Commander"],
        created_at=now,
        updated_at=now,
        logs=[],
        metrics={
            "cpu": random.randint(40, 98),
            "memory": random.randint(45, 96),
            "disk": random.randint(30, 95),
            "latency_ms": random.randint(40, 500),
        },
    )


def generate_log(incident_id: str) -> LogEntry:
    log_messages = [
        "kernel: disk I/O error",
        "systemd: service restarted",
        "nginx: upstream timed out",
        "auth: failed login attempts",
        "app: exception in worker thread",
    ]
    return LogEntry(
        id=str(uuid4()),
        incident_id=incident_id,
        level=random.choice(["INFO", "WARN", "ERROR"]),
        message=random.choice(log_messages),
        timestamp=datetime.utcnow(),
    )
