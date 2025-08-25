from typing import Literal

from pydantic import BaseModel
from pydantic import DirectoryPath

from .base import PROJECT_DIR


class LogConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    folder: DirectoryPath = PROJECT_DIR / ".logs"
