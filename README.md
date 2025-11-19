# akamai-wrapper-pub

Shared Akamai utilities for Python projects. This package provides common functionality for interacting with Akamai APIs across multiple projects.

## Features

- **Akamai API Client**: Base class with EdgeGrid authentication
- **CLI Tools**: Command-line utilities for common tasks
  - `search-asw`: Search for account switch keys

## Install with uv

```bash
# Add as a regular dependency
uv add akamai-wrapper-pub

# Or for development in editable mode
uv add --editable ../akamai-wrapper-pub
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

## License

Licensed under the MIT License. See `LICENSE` for details.
