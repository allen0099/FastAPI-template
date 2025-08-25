from dataclasses import field
from logging import Logger
from logging import getLogger
from typing import Annotated
from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import BeforeValidator
from pydantic import Field
from pydantic import SecretStr

logger: Logger = getLogger(__name__)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, list):
        return v

    if isinstance(v, str):
        if v == "*":
            return v

        if (v.startswith("[") and v.endswith("]")) or (v.startswith("(") and v.endswith(")")):
            return [i.strip('"').strip() for i in v[1:-1].split(",")]

        if not v.startswith("["):
            return [i.strip() for i in v.split(",")]

    raise ValueError(v)


class ProjectConfig(BaseModel):
    title: str = "Project FastAPI"
    environment: Literal["development", "staging", "production"] = "development"
    project_key: SecretStr = Field(alias="secret_key")  # The key used for session and JWT

    cors_origins: Annotated[list[str | Literal["*"]] | str, BeforeValidator(parse_cors)] = field(default_factory=list)
