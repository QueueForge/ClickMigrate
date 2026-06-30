# Contributing to ClickMigrate

Thank you for your interest in contributing to **ClickMigrate**! Contributions of all kinds are welcome, including bug reports, feature requests, documentation improvements, and code contributions.

## Getting Started

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/queueforge/ClickMigrate.git
cd ClickMigrate

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

## Building the Project

To build the package locally, run:

```bash
python -m build
```

The generated distribution files will be placed in the `dist/` directory.

## Code Style

Before opening a pull request, please ensure your code is formatted and passes the basic checks.

Format the code:

```bash
black .
```

Lint the project:

```bash
ruff check .
```

Type check:

```bash
mypy .
```

## Testing

An automated test suite has not been implemented yet.

For now, please manually verify that your changes work as expected and do not introduce regressions. A comprehensive testing framework will be added in a future release.

## Pull Requests

Before submitting a pull request:

* Keep changes focused on a single feature or bug fix.
* Write clear and descriptive commit messages.
* Update the documentation if your changes affect user-facing behavior.
* Ensure the project builds successfully.

## Commit Messages

Please follow the commit message format below:

```text
<type>(<module>): <short description>
```

If the change affects multiple modules or the entire project, omit the module name:

```text
<type>: <short description>
```

### Commit Types

| Type       | Description                                           |
| ---------- | ----------------------------------------------------- |
| `feat`     | A new feature                                         |
| `fix`      | A bug fix                                             |
| `refactor` | Code improvements without changing behavior           |
| `style`    | Formatting, comments, or other non-functional changes |
| `docs`     | Documentation changes                                 |
| `test`     | Adding or updating tests                              |
| `chore`    | Maintenance tasks, dependencies, CI, tooling, etc.    |

### Examples

```text
feat(cli): add rollback command
fix(database): handle missing migration table
refactor(manager): simplify migration discovery
style(manager): add explicit type annotations
docs: update installation guide
test(database): add migration manager tests
chore: update GitHub Actions workflow
```

Keep commit messages concise, descriptive, and written in the imperative mood.

## Reporting Issues

If you discover a bug or have a feature request, please open an issue with as much detail as possible, including:

* ClickMigrate version
* ClickHouse version
* Python version
* Operating system
* Steps to reproduce the issue

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
