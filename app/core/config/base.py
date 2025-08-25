from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import YamlConfigSettingsSource
from pydantic_settings.sources import PathType
from pydantic_settings.sources.types import DEFAULT_PATH

PROJECT_DIR: Path = Path(__file__).parent.parent.parent.parent


class ExtraYamlConfigSettingsSource(YamlConfigSettingsSource):
    def __init__(
        self,
        settings_cls: type[BaseSettings],
        yaml_file: PathType | None = DEFAULT_PATH,
        yaml_file_encoding: str | None = None,
    ) -> None:
        self.settings_cls = settings_cls
        self.config = settings_cls.model_config
        super().__init__(settings_cls, yaml_file, yaml_file_encoding)

    def _process_dict_case_sensitivity(self, data: dict[str, Any], case_sensitive: bool) -> dict[str, Any]:
        if case_sensitive:
            return data

        result = {}
        for key, value in data.items():
            if isinstance(key, str):
                # Add both uppercase and lowercase keys
                lower_key = key.lower()
                upper_key = key.upper()
                if isinstance(value, dict):
                    processed_value = self._process_dict_case_sensitivity(value, case_sensitive)
                    result[lower_key] = processed_value
                    result[upper_key] = processed_value
                else:
                    result[lower_key] = value
                    result[upper_key] = value
            # For non-string keys, keep them as is
            elif isinstance(value, dict):
                result[key] = self._process_dict_case_sensitivity(value, case_sensitive)
            else:
                result[key] = value
        return result

    def _read_file(self, file_path: Path) -> dict[str, Any]:
        raw: dict[str, Any] = super()._read_file(file_path)
        case_sensitive: bool = self.config.get("case_sensitive", False)

        # Process case sensitivity
        raw = self._process_dict_case_sensitivity(raw, case_sensitive)

        if self.settings_cls.model_config.get("env_prefix", None):
            prefix = self.settings_cls.model_config["env_prefix"].strip("_")
            if not case_sensitive:
                prefix = prefix.lower()
            return raw.get(prefix, {})

        return raw


def get_configs(**kwargs: Any) -> SettingsConfigDict:
    return SettingsConfigDict(
        case_sensitive=False,
        env_file=PROJECT_DIR / ".env",
        env_ignore_empty=True,
        env_nested_delimiter="__",
        yaml_file=PROJECT_DIR / "env.yaml",
        extra="ignore",
        **kwargs,
    )


class Reload:
    def reload(self) -> None:
        """Helper function to reload the settings."""
        # See: https://docs.pydantic.dev/latest/concepts/pydantic_settings/#in-place-reloading
        self.__init__()


class ProjectBaseSettings(BaseSettings, Reload):
    model_config = SettingsConfigDict(
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            ExtraYamlConfigSettingsSource(settings_cls),
            *super().settings_customise_sources(
                settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings
            ),
        )
