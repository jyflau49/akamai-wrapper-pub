# Development Guide

**Last modified: 2025-11-19**

## Setup

```bash
# Clone and install dependencies
cd akamai-wrapper-pub
uv sync

# Install pre-commit hooks
pre-commit install
```

## Pre-commit Hooks

This project uses pre-commit with Trivy security scanning:

- **trivy-fs**: Filesystem vulnerability scan (HIGH/CRITICAL)
- **trivy-config**: Configuration security scan (HIGH/CRITICAL)

### Requirements

- [Trivy](https://trivy.dev/) must be installed on your system
- Install via: `brew install trivy` (macOS) or see [Trivy installation docs](https://aquasecurity.github.io/trivy/latest/getting-started/installation/)

### Running Manually

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run Trivy scans directly
trivy fs --severity HIGH,CRITICAL .
trivy config --severity HIGH,CRITICAL .
```

## Testing

```bash
# Run tests (when available)
uv run pytest

# Test CLI
uv run search-asw --help
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Keep functions focused and simple (DRY principle)
- Document public APIs with docstrings

## Release Process

1. Update version in `pyproject.toml` and `src/akamai_wrapper_pub/__init__.py`
2. Update `docs/CHANGELOG.md`
3. Commit changes: `git commit -m "Release vX.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push && git push --tags`
