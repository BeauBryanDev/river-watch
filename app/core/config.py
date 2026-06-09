# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):

    # general
    ENVIRONMENT:          str  = "development"
    PROJECT_NAME:         str  = "RiverWatch"
    VERSION:              str  = "0.1.0"

    # database
    DATABASE_URL:         str

    # models
    MODEL_SEGFORMER_PATH: str  = "weights/best_model.pt"
    MODEL_RAFT_PATH:      str  = "weights/raft_small.pth"
    NUM_CLASSES:          int  = 7
    WATER_CLASS_INDEX:    int  = 1

    # pipeline
    SEGFORMER_INTERVAL:   int  = 100
    FRAME_DIFF_THRESHOLD: float = 15.0
    TARGET_WIDTH:         int  = 512
    ANOMALY_Z_THRESHOLD:  float = 2.0
    SLIDING_WINDOW_SIZE:  int  = 150

    # upload
    UPLOAD_DIR:           str  = "/tmp/riverwatch_uploads"
    MAX_VIDEO_MB:         int  = 500

    # cors
    ALLOWED_ORIGINS:      List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()