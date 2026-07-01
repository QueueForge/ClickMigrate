"""Command Line Interface for ClickMigrate."""

import os
import typer
from rich.console import Console
from rich.markup import escape
from clickmigrate.config import load_config, create_config
from clickmigrate.manager import MigrationManager
from clickmigrate.exceptions import ClickMigrateError
from importlib.metadata import version as get_version

app = typer.Typer(help="ClickMigrate: A modern ClickHouse migration framework.")
console = Console()


def get_manager() -> MigrationManager:
    try:
        config = load_config()
        return MigrationManager(config)
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """Print the current ClickMigrate version."""

    console.print(f"[green]ClickMigrate version: {get_version('clickmigrate')}[/green]")


@app.command()
def init() -> None:
    """Initialize a new ClickMigrate environment."""

    try:
        create_config()
        console.print("[green]Added ClickMigerate config to pyproject.toml[/green]")
    except Exception as e:
        console.print(f"[red]{escape(str(e))}[/red]")

    config = load_config()

    os.makedirs(config.migration_directory, exist_ok=True)

    console.print(
        f"[green]Initialized ClickMigrate in ./{config.migration_directory}/[/green]"
    )


@app.command()
def revision(
    message: str = typer.Option(..., "-m", "--message", help="Migration description")
) -> None:
    """Create a new migration file."""
    manager = get_manager()
    filepath = manager.create_revision(message)
    console.print(f"[green]Created revision:[/green] {filepath}")


@app.command()
def migrate(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Simulate migration without applying"
    )
) -> None:
    """Apply all pending migrations."""
    console.print("\n[bold]ClickMigrate[/bold]\n")

    manager = get_manager()

    try:
        manager.validate()

        pending = manager.get_pending_migrations()
        total = len(pending)

        if total == 0:
            console.print("No pending migrations.\n")
            return

        console.print(f"Applying [yellow]{total}[/yellow] migrations...\n")

        if dry_run:
            console.print("[yellow]DRY RUN: no changes will be applied.\n")

        elapsed = 0.0

        for i, migration in enumerate(pending, start=1):
            duration = manager.migrate(migration, dry_run=dry_run)
            elapsed += duration

            console.print(
                f"[green]SUCCESS[/green] {migration.version}_{migration.name} "
                f"({i}/{total}) in {duration:.2f}s"
            )

        console.print("\n[bold green]DONE[/bold green]\n")
        console.print(f"Applied migrations : {total}")
        console.print("Pending migrations : 0")
        console.print(f"Execution time     : {elapsed:.2f}s\n")

    except ClickMigrateError as e:
        console.print(f"\n[bold red]FAILED[/bold red]\n{e}")
        raise typer.Exit(code=1)


@app.command()
def status() -> None:
    """Show current migration status."""
    manager = get_manager()
    applied, pending = manager.status()
    console.print(f"Applied migrations : [green]{applied}[/green]")
    console.print(f"Pending migrations : [yellow]{pending}[/yellow]")

    pending_migrations = manager.get_pending_migrations()

    for m in pending_migrations:
        console.print(f"- Version: {m.version}; Name: {m.name}")


@app.command()
def validate() -> None:
    """Validate checksums of applied migrations against local files."""
    manager = get_manager()
    try:
        manager.validate()
        console.print(
            "[green]All migrations are valid. No checksum mismatches.[/green]"
        )
    except ClickMigrateError as e:
        console.print(f"[bold red]Validation Failed:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
