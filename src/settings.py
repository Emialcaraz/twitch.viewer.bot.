from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, BaseSettings, root_validator, validator

import version


class LogLevelEnum(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class EnvironmentTypeEnum(str, Enum):
    production = "production"
    development = "development"


class Settings(BaseSettings):
    VERSION = version.__version__
    ENV_TYPE = EnvironmentTypeEnum.production

    # Twitch
    TWITCH_URL: str

    # Logging
    LOG_FILE: str = "log"
    LOG_LEVEL: LogLevelEnum = LogLevelEnum.info
    LOGGER_MSG_FORMAT: str = "%(name)s :: %(levelname)s :: %(message)s"


settings = Settings()
