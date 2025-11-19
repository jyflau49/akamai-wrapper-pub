# akamai-wrapper-pub

Shared Akamai utilities for Python projects. This package provides common functionality for interacting with Akamai APIs across multiple projects.

## Features

- **Akamai API Client**: Base class with EdgeGrid authentication
- **CLI Tools**: Command-line utilities for common tasks
  - `search-asw`: Search for account switch keys

## Installation

### For Development (Editable Mode)

Install in your project with editable mode to enable live updates:

```bash
# From your project directory
uv add --editable ../akamai-wrapper-pub
```

### As a Regular Dependency

```bash
uv add akamai-wrapper-pub
```

## Usage

### As a Library

```python
from akamai_wrapper_pub import Akamai

# Initialize client
client = Akamai(
    edgerc_path="~/.edgerc",
    section="default",
    timeout=30
)

# Make API calls
result = client.get('/identity-management/v3/api-clients/self/account-switch-keys')
```

### CLI Tools

#### Account Search

Search for Akamai account-switch-key:

```bash
# Basic search
uv run search-asw "Account Name"

# With custom edgerc section
uv run search-asw --section production "Account Name"

# With verbose logging
uv run search-asw --verbose "Account Name"
```

## Development

```bash
# Clone and install
cd akamai-wrapper-pub
uv sync

# Install pre-commit hooks (requires Trivy)
pre-commit install
```

For detailed development setup, testing, and contribution guidelines, see [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md).

## API Reference

### `Akamai` Class

Main API client with EdgeGrid authentication.

**Methods:**
- `__init__(edgerc_path, section, timeout, account_switch_key)` - Initialize client
- `get(path, query, params)` - Make GET request
- `put(path, data, params)` - Make PUT request
- `FromOptions(options)` - Create from argparse options (classmethod)

See inline docstrings for detailed parameter documentation.

## Requirements

- Python 3.9+
- Dependencies: `edgegrid-python`, `requests`, `tabulate` (see `pyproject.toml`)

## License

Licensed under the MIT License. See `LICENSE` for details.
