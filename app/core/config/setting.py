from pathlib import Path

from pydantic import Field

from .base import PROJECT_DIR
from .base import ProjectBaseSettings
from .base import get_configs
from .log import LogConfig
from .project import ProjectConfig


class Settings(ProjectBaseSettings):
    model_config = get_configs()

    project: ProjectConfig
    log: LogConfig = Field(default=LogConfig())

    @property
    def PROJECT_DIR(self) -> Path:  # noqa: N802
        return PROJECT_DIR
