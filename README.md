# ClickMigrate

A modern, lightweight, and reliable database migration framework for ClickHouse, inspired by Alembic.

ClickMigrate provides a clean CLI and Python API for managing ClickHouse schema migrations without unnecessary complexity.

## About

**ClickMigrate** is an open-source project developed and maintained by **QueueForge**. It is designed to provide a modern, simple, and reliable migration framework for ClickHouse databases. Learn more about QueueForge at https://queueforge.dev.

---

## Features

- **SQL-based Migrations** – Write your migrations in plain `.sql` files.
- **Automatic Ordering** – Lexicographical sorting ensures migrations run in the correct sequence.
- **State Management** – Automatically creates and manages a migration history table in ClickHouse.
- **Checksum Validation** – Validates SHA-256 checksums to detect modified applied migrations.
- **Flexible Configuration** – Supports `pyproject.toml`, JSON, YAML, or environment variables.
- **Project Initialization** – `clickmigrate init` automatically creates a `pyproject.toml` configuration file with sensible defaults.
- **Dry-Run Mode** – Preview which migrations will be applied without altering the database.
- **Python API & CLI** – Use ClickMigrate from your terminal or programmatically in Python.
- **Version Command** – Display the installed ClickMigrate version with `clickmigrate version`.

---

# Installation

ClickMigrate requires **Python 3.11+**.

Install it using pip:

```bash
pip install ClickMigrate
````

---

# Quick Start (CLI)

ClickMigrate provides an Alembic-like CLI for managing your migration workflow.

## 1. Initialize the Environment

Create the migration directory (default: `migrations/`) and generate a `pyproject.toml` configuration file with default settings if one does not already exist.

```bash
clickmigrate init
```

---

## 2. Create a Revision

Generate a new sequential SQL migration file.

```bash
clickmigrate revision -m "create users table"
```

Example output:

```text
migrations/
└── 001_create_users_table.sql
```

Edit the generated file and add your ClickHouse SQL statements.

---

## 3. Check Status

View applied and pending migrations, including the version and name of each pending migration.

```bash
clickmigrate status
```

---

## 4. Apply Migrations

Run all pending migrations. Progress and execution time are displayed for each migration.

```bash
clickmigrate migrate
```

Preview the execution without applying changes:

```bash
clickmigrate migrate --dry-run
```

---

## 5. Validate Migration Integrity

Verify that previously applied migration files have not been modified.

```bash
clickmigrate validate
```

---

## 6. Show Version

Display the installed ClickMigrate version.

```bash
clickmigrate version
```

---

# Configuration

ClickMigrate automatically searches for configuration files in your project root.

Supported formats (in priority order):

1. `pyproject.toml` *(recommended)*
2. `clickmigrate.json`
3. `clickmigrate.yaml`
4. Environment variables

## Option A: `pyproject.toml` (Recommended)

```toml
[tool.clickmigrate]
host = "localhost"
port = 8123
database = "default"
username = "default"
password = "your_secure_password"

migration_directory = "migrations"
migration_table = "clickmigrate_history"
```

## Option B: `clickmigrate.json`

```json
{
  "host": "localhost",
  "port": 8123,
  "database": "default",
  "username": "default",
  "password": "your_secure_password",
  "migration_directory": "migrations",
  "migration_table": "clickmigrate_history"
}
```

## Option C: `clickmigrate.yaml`

```yaml
host: localhost
port: 8123
database: default
username: default
password: your_secure_password

migration_directory: migrations
migration_table: clickmigrate_history
```

## Option D: Environment Variables

```bash
CLICKMIGRATE_HOST=localhost
CLICKMIGRATE_PORT=8123
CLICKMIGRATE_DATABASE=default
CLICKMIGRATE_USERNAME=default
CLICKMIGRATE_PASSWORD=your_secure_password

CLICKMIGRATE_MIGRATION_DIRECTORY=migrations
CLICKMIGRATE_MIGRATION_TABLE=clickmigrate_history
```

---

# Migration Naming

Migration files are executed in **lexicographical order**.

Example:

```text
001_create_users.sql
002_add_email.sql
003_create_orders.sql
004_add_indexes.sql
```

Each migration is executed only once and recorded in the migration history table.

---

# Commands

| Command                              | Description                             |
| ------------------------------------ | --------------------------------------- |
| `clickmigrate init`                  | Initialize a migration project          |
| `clickmigrate revision -m "message"` | Create a new migration                  |
| `clickmigrate status`                | Show applied and pending migrations     |
| `clickmigrate migrate`               | Apply pending migrations                |
| `clickmigrate migrate --dry-run`     | Preview pending migrations              |
| `clickmigrate validate`              | Validate migration checksums            |
| `clickmigrate version`               | Show the installed ClickMigrate version |
| `clickmigrate help`                  | Show the CLI help message               |

---

# Requirements

- Python **3.11+**
- A running ClickHouse server
- HTTP interface enabled (default port `8123`)

---

# License

MIT License.