import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://arcsight:arcsight@localhost:5432/arcsight3d")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.getenv("UPLOAD_FOLDER", "uploads"))
    EXPORT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.getenv("EXPORT_FOLDER", "exports"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_MB", 20)) * 1024 * 1024
    
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", "")
    BLENDER_EXECUTABLE = os.getenv("BLENDER_EXECUTABLE", "blender")
    UNITY_EXECUTABLE = os.getenv("UNITY_EXECUTABLE", "unity")
    
    DEFAULT_SCALE_FACTOR = float(os.getenv("DEFAULT_SCALE_FACTOR", 0.05))
    DEFAULT_WALL_HEIGHT = float(os.getenv("DEFAULT_WALL_HEIGHT", 3.0))
    DEFAULT_WALL_THICKNESS = float(os.getenv("DEFAULT_WALL_THICKNESS", 0.15))

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    DEBUG = False
    # Use real production URIs, etc.
    
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
