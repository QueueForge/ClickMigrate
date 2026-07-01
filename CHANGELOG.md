# Changelog

---

## **v1.0.3 – 2026-07-01**

### Fixed

* Prevented a path traversal issue in `create_revision()`.
* Hardened the database layer against SQL injection.

### Refactored

* Refactored the codebase using **Black**, **Ruff**, and **MyPy**.

### Documentation

* Added an **About** section to the README.
* Added a `CONTRIBUTING.md` guide.
* Added a `CODE_OF_CONDUCT.md`.
* Added this `CHANGELOG.md`.

### Security Notes

The path traversal issue had no practical security impact under normal usage. Exploitation would require an attacker to already be able to invoke `create_revision()` with a controlled migration message and have sufficient file system permissions to write files outside the migration directory.

Likewise, the SQL injection issue had no practical security impact. Exploitation would require an attacker to already control the application's database configuration (including the migration table name) or otherwise possess privileges sufficient to execute arbitrary SQL statements.

---

## **v1.0.0 – 2026-06-30**

Initial release of ClickMigrate, featuring checksum validation, configuration management, a command-line interface (CLI), migration creation and execution, and migration status tracking.