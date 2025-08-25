from pydantic import SecretStr
from pydantic import computed_field

from .base import ProjectBaseSettings
from .base import get_configs


class EmailSettings(ProjectBaseSettings):
    model_config = get_configs(env_prefix="EMAIL_")

    SMTP_TLS: bool = False
    SMTP_STARTTLS: bool = False

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: SecretStr = ""

    FROM_EMAIL: str = ""
    FROM_NAME: str = "Project FastAPI"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def enabled(self) -> bool:
        return bool(self.SMTP_USER and self.SMTP_PASSWORD.get_secret_value())


# By environment variables (case-insensitive)
# EMAIL_SMTP_TLS=True

# Or by a .env file (case-insensitive)
# EMAIL_SMTP_TLS=True

# Or by a .yaml file (case-insensitive)
# email:
#   smtp_tls: true
