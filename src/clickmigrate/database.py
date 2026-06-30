"""Database interaction layer."""

import clickhouse_connect
from clickhouse_connect.driver.client import Client
from typing import List, Dict, Any
from clickmigrate.config import Config
from clickmigrate.exceptions import MigrationError


class Database:
    """Handles ClickHouse connections and queries."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.client: Client = self._connect()

    def _connect(self) -> Client:
        """Establishes a connection to ClickHouse."""
        try:
            return clickhouse_connect.get_client(
                host=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                database=self.config.database,
            )
        except Exception as e:
            raise MigrationError(f"Failed to connect to ClickHouse: {e}")

    def ensure_history_table(self) -> None:
        """Creates the migration history table if it doesn't exist."""
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.config.migration_table} (
            version String,
            name String,
            checksum String,
            applied_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY version
        """
        self.client.command(query)

    def get_applied_migrations(self) -> Dict[str, str]:
        """Retrieves applied migrations and their checksums.

        Returns:
            Dict mapping version to checksum.
        """
        self.ensure_history_table()
        query = f"SELECT version, checksum FROM {self.config.migration_table}"
        result = self.client.query(query)
        return {row[0]: row[1] for row in result.result_rows}

    def apply_migration(self, version: str, name: str, checksum: str, sql: str) -> None:
        """Executes a migration script and records it in the history table."""
        try:
            # Execute the actual migration
            self.client.command(sql)

            # Record in history
            record_query = f"""
            INSERT INTO {self.config.migration_table} (version, name, checksum)
            VALUES ('{version}', '{name}', '{checksum}')
            """
            self.client.command(record_query)
        except Exception as e:
            raise MigrationError(f"Failed to apply migration {version}_{name}: {e}")
