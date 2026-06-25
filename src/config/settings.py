import os
from dataclasses import dataclass
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
env_file_path = os.path.join(project_root, ".env")

load_dotenv(env_file_path, verbose=True)

@dataclass(frozen=True)
class BaseConfig:
    """共通の定数"""
    TIME = r"([0-2][0-3]|[0-1][0-9]):[0-5][0-9]|(0[0-9]|[1-9]):[0-5][0-9]"
    DATETIME = r"((0[1-9]|[1-9])|1[0-2])/(0[1-9]|[1-9]|[12][0-9]|3[01])/(([0-2][0-3]|[0-1][0-9]):[0-5][0-9]|(0[0-9]|[1-9]):[0-5][0-9])"
    YEARDATETIME = r"[0-9]{4}/((0[1-9]|[1-9])|1[0-2])/(0[1-9]|[1-9]|[12][0-9]|3[01])/(([0-2][0-3]|[0-1][0-9]):[0-5][0-9]|(0[0-9]|[1-9]):[0-5][0-9])"
    DATETIME_TYPE = r"(([0-2][0-3]|[0-1][0-9]):[0-5][0-9]|(0[0-9]|[1-9]):[0-5][0-9])|((0[1-9]|[1-9])|1[0-2])/(0[1-9]|[1-9]|[12][0-9]|3[01])/(([0-2][0-3]|[0-1][0-9]):[0-5][0-9]|(0[0-9]|[1-9]):[0-5][0-9])|([0-9]{4})/((0[1-9]|[1-9])|1[0-2])/(0[1-9]|[1-9]|[12][0-9]|3[01])/(([0-2][0-3]|[0-1][0-9]):[0-5][0-9]|(0[0-9]|[1-9]):[0-5][0-9])"
    HERE_MENTION = "@here"
    EVE_MENTION = "@everyone"

@dataclass(frozen=True)
class DevelopmentConfig(BaseConfig):
    """開発環境用の固有設定"""
    DEBUG_MODE: bool = True
    AUTO_DEADLINE = 300

@dataclass(frozen=True)
class ProductionConfig(BaseConfig):
    """本番環境用の固有設定"""
    DEBUG_MODE: bool = False
    AUTO_DEADLINE = 10800

# --------------------------------------------------
# 環境の判定とエクスポート
# --------------------------------------------------
_env = os.getenv("EXECUTION_ENV")

if _env == "PRODUCTION":
    env_c = ProductionConfig()
    TOKEN = os.getenv("PRODUCTION_TOKEN")
else:
    env_c = DevelopmentConfig()
    TOKEN = os.getenv("DEVELOPMENT_TOKEN")