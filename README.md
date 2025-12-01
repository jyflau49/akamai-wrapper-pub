# akamai-wrapper-pub

Lightweight Akamai CLI utilities and Python API client with EdgeGrid authentication.

## Features

- **API Client**: Python client with EdgeGrid auth supporting GET/POST/PUT/PATCH/DELETE
- **CLI Tools**:
  - `search-asw` - Search for account switch keys
  - `search-group` - Search for groups by name
  - `list-properties` - List all properties with version info
  - `download-property` - Download property rules to JSON
  - `download-properties` - Download all property rules to JSON files

## Installation

```bash
uv add akamai-wrapper-pub
```

## CLI Usage

All commands support these common options:
- `-k, --account-switch-key` - Account switch key for multi-account access
- `-t, --timeout` - Request timeout in seconds (default: 30)
- `--edgerc` - Path to .edgerc file (default: ~/.edgerc)
- `--section` - Section in .edgerc (default: default)
- `--verbose` - Enable verbose output

### search-asw

Search for account switch keys by name:

```bash
uv run search-asw "Account Name"
```

### search-group

Search for groups by name (case-insensitive partial match):

```bash
uv run search-group "Group Name"
uv run search-group -k 1-ABCDE:1-12345 "Hong Kong"
```

### list-properties

List all properties with version info:

```bash
uv run list-properties
uv run list-properties -g grp_123456      # Filter by group ID
uv run list-properties -k 1-ABCDE:1-12345 # With account switch key
```

### download-property

Download property rules to JSON:

```bash
uv run download-property prp_123456
uv run download-property prp_123456 -v 5         # Specific version
uv run download-property prp_123456 -o out.json  # Custom output file
```

### download-properties

Download all property rules to JSON files (uses production version if available, otherwise latest):

```bash
uv run download-properties
uv run download-properties -g grp_123456    # Filter by group ID
uv run download-properties -o ./output      # Custom output directory
uv run download-properties --delay 1.0      # Slower rate limiting
```

## Library Usage

```python
from akamai_wrapper_pub import Akamai

client = Akamai(edgerc_path="~/.edgerc", section="default")

# GET request
result = client.get('/papi/v1/groups')

# POST request with body
result = client.post('/papi/v1/search/find-by-value', data={"propertyName": "example"})
```

## Development

```bash
uv sync
pre-commit install
```

## License

MIT
