"""Core migration management logic."""

import os
import hashlib
import time
from typing import List, Tuple
from dataclasses import dataclass
from clickmigrate.config import Config
from clickmigrate.database import Database
from clickmigrate.exceptions import ChecksumError


@dataclass
class Migration:
    """Represents a single SQL migration."""

    version: str
    name: str
    filepath: str
    content: str
    checksum: str


class MigrationManager:
    """API for managing ClickHouse migrations."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.db = Database(config)

    def _calculate_checksum(self, content: str) -> str:
        """Calculates SHA-256 checksum for migration content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _get_local_migrations(self) -> List[Migration]:
        """Discovers and parses local .sql migration files."""
        migrations = []
        if not os.path.exists(self.config.migration_directory):
            return migrations

        for filename in sorted(os.listdir(self.config.migration_directory)):
            if filename.endswith(".sql"):
                parts = filename.replace(".sql", "").split("_", 1)
                if len(parts) != 2:
                    continue

                version, name = parts
                filepath = os.path.join(self.config.migration_directory, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                checksum = self._calculate_checksum(content)
                migrations.append(Migration(version, name, filepath, content, checksum))

        return migrations

    def validate(self) -> None:
        """Validates that local checksums match applied checksums."""
        applied = self.db.get_applied_migrations()
        local = self._get_local_migrations()

        for loc in local:
            if loc.version in applied:
                if applied[loc.version] != loc.checksum:
                    raise ChecksumError(
                        f"Checksum mismatch for {loc.version}_{loc.name}. "
                        "The local file has been modified since it was applied."
                    )

    def status(self) -> Tuple[int, int]:
        """Returns the count of (applied, pending) migrations."""
        applied = self.db.get_applied_migrations()
        local = self._get_local_migrations()
        pending_count = sum(1 for m in local if m.version not in applied)
        return len(applied), pending_count

    def migrate(self, dry_run: bool = False) -> Tuple[int, float]:
        """Applies all pending migrations.

        Returns:
            Tuple containing (number of migrations applied, execution time in seconds).
        """
        self.validate()
        applied_map = self.db.get_applied_migrations()
        local = self._get_local_migrations()

        pending = [m for m in local if m.version not in applied_map]

        if dry_run or not pending:
            return len(pending), 0.0

        start_time = time.time()
        for migration in pending:
            self.db.apply_migration(
                version=migration.version,
                name=migration.name,
                checksum=migration.checksum,
                sql=migration.content,
            )

        return len(pending), time.time() - start_time

    def create_revision(self, message: str) -> str:
        """Creates a new empty migration file."""
        os.makedirs(self.config.migration_directory, exist_ok=True)
        local = self._get_local_migrations()

        next_version = 1 if not local else int(local[-1].version) + 1
        version_str = f"{next_version:03d}"

        safe_name = message.lower().replace(" ", "_").replace("-", "_")
        filename = f"{version_str}_{safe_name}.sql"
        filepath = os.path.join(self.config.migration_directory, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"-- Migration: {message}\n-- Version: {version_str}\n\n")

        return filepath
