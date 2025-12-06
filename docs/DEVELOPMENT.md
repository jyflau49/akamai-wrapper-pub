# Development Guide

**Last modified: 2025-12-06**

## Setup

```bash
# Clone and install dependencies
cd akamai-wrappy
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
