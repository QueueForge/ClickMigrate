"""ClickMigrate - A database migration framework for ClickHouse."""

from clickmigrate.manager import MigrationManager
from clickmigrate.config import Config

__all__ = ["MigrationManager", "Config"]