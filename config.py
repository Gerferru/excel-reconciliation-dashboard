import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    SMTP_HOST: str = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() in ("true", "1", "yes")

    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "alertas@empresa.com")
    EMAIL_TO: list[str] = [
        email.strip() for email in os.getenv("EMAIL_TO", "").split(",") if email.strip()
    ]
    EMAIL_SUBJECT_PREFIX: str = os.getenv("EMAIL_SUBJECT_PREFIX", "[AUDITORÍA EXCEL]")

settings = Settings()
