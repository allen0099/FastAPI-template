import json
import logging.config
import os
from pathlib import Path
from typing import Any, Optional

import yaml

base_folder: Path = Path(__file__).parent.parent.parent
logger_config: Optional[Path] = None

_env_file: Path = base_folder / "environments.json"
_variables: dict[str, Any] = {
    "HOST": "0.0.0.0",
    "PORT": 8000,
}  # Loader

if os.path.isfile(_env_file):
    with open(_env_file, "r", encoding="utf-8") as f:
        # We use update to merge the dict
        # and use the environment variables to overwrite the config file
        _variables.update(json.load(f))


def _load_logger(logger_name: str = "logger") -> None:
    """
    Load the logger config from the files.

    Args:
        logger_name: The name of the logger config file

    Returns:
        None
    """
    global logger_config

    yml_config: Path = base_folder / f"{logger_name}.yml"
    yaml_config: Path = base_folder / f"{logger_name}.yaml"
    json_config: Path = base_folder / f"{logger_name}.json"

    if os.path.exists(yml_config):
        with open(yml_config) as file:
            loaded_config: dict[Any] = yaml.safe_load(file)
            logging.config.dictConfig(loaded_config)
            logger_config = yml_config
            return

    if os.path.exists(yaml_config):
        with open(yaml_config) as file:
            loaded_config: dict[Any] = yaml.safe_load(file)
            logging.config.dictConfig(loaded_config)
            logger_config = yaml_config
            return

    if os.path.exists(json_config):
        with open(json_config) as file:
            loaded_config: dict[Any] = json.load(file)
            logging.config.dictConfig(loaded_config)
            logger_config = json_config


def get(key: str, default: Any = None) -> Any:
    """
    Get the value of the key from the config file, if not found, return the default value

    Args:
        key: The key of the config
        default: The default value if the key is not found

    Returns:
        Any: The value of the key
    """
    env: Any = os.getenv(key)

    if env is not None:
        return env

    if key in _variables and _variables[key] is not None:
        return _variables[key]

    else:
        return default


_load_logger()
