from logging import Logger
from logging import getLogger

from pydantic_core import ValidationError

from .email import EmailSettings
from .setting import Settings
from .setting import get_configs

logger: Logger = getLogger(__name__)

try:
    settings: Settings = Settings()  # type: ignore
    email: EmailSettings = EmailSettings()

except ValidationError as e:
    output: str = f"{e.error_count()} validation errors while loading settings\n\n"
    for error in e.errors(include_url=False):
        output += f"{'.'.join(error['loc'])}\n  {error['type']} -> {error['msg']}\n"
    logger.error(output)
    raise ValueError() from None
