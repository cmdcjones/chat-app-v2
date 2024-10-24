import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'secret')
    DEBUG: bool = os.getenv('DEBUG', False)
    ALLOWED_HOSTS: list[str] = field(default_factory=lambda: os.getenv('ALLOWED_HOSTS', '').split(','))