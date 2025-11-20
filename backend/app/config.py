from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/smarthire_db"
    
    # JWT
    SECRET_KEY: str = "changeme"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Upload directories
    UPLOAD_DIR: str = "./uploads"
    AVATAR_DIR: str = "./uploads/avatars"
    CV_DIR: str = "./uploads/cvs"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # Scraping
    SCRAPING_ENABLED: bool = True
    SCRAPING_MAX_OFFERS: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


# Créer les dossiers uploads s'ils n'existent pas
def create_upload_dirs():
    dirs = [
        settings.UPLOAD_DIR,
        settings.AVATAR_DIR,
        settings.CV_DIR,
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory created/verified: {dir_path}")


