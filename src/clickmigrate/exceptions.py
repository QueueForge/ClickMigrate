"""Custom exceptions for ClickMigrate."""


class ClickMigrateError(Exception):
    """Base exception for all ClickMigrate errors."""

    pass


class ConfigurationError(ClickMigrateError):
    """Raised when configuration is invalid or missing."""

    pass


class MigrationError(ClickMigrateError):
    """Raised when a migration fails to apply."""

    pass


class ChecksumError(ClickMigrateError):
    """Raised when an applied migration's checksum differs from the file."""

    pass
