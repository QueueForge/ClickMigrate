"""Configuration management for ClickMigrate."""

import os
import json
import tomllib
from dataclasses import dataclass
from typing import Any, Dict
import yaml
from clickmigrate.exceptions import ConfigurationError

@dataclass
class Config:
    """Stores the ClickMigrate configuration."""
    host: str = "localhost"
    port: int = 8123
    database: str = "default"
    username: str = "default"
    password: str = ""
    migration_directory: str = "migrations"
    migration_table: str = "clickmigrate_history"

def load_config() -> Config:
    """Loads configuration from environment variables or files."""
    config_data: Dict[str, Any] = {}

    # 1. Try pyproject.toml
    if os.path.exists("pyproject.toml"):
        with open("pyproject.toml", "rb") as f:
            toml_data = tomllib.load(f)
            config_data.update(toml_data.get("tool", {}).get("clickmigrate", {}))

    # 2. Try clickmigrate.json
    elif os.path.exists("clickmigrate.json"):
        with open("clickmigrate.json", "r") as f:
            config_data.update(json.load(f))

    # 3. Try clickmigrate.yaml
    elif os.path.exists("clickmigrate.yaml"):
        with open("clickmigrate.yaml", "r") as f:
            config_data.update(yaml.safe_load(f) or {})

    # 4. Override with Environment Variables
    env_mapping = {
        "CLICKMIGRATE_HOST": "host",
        "CLICKMIGRATE_PORT": "port",
        "CLICKMIGRATE_DATABASE": "database",
        "CLICKMIGRATE_USERNAME": "username",
        "CLICKMIGRATE_PASSWORD": "password",
        "CLICKMIGRATE_DIRECTORY": "migration_directory",
        "CLICKMIGRATE_TABLE": "migration_table",
    }
    
    for env_var, key in env_mapping.items():
        if env_var in os.environ:
            val = os.environ[env_var]
            config_data[key] = int(val) if key == "port" else val

    return Config(**config_data)