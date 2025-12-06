# akamai-wrappy

Lightweight Akamai CLI utilities and Python API client with EdgeGrid authentication.

## Features

- **CLI Tools** (via `awp` command):
  - `search-asw` - Search for account switch keys
  - `search-group` - Search for groups by name
  - `list-properties` - List all properties with version info
  - `download-property` - Download property rules to JSON
  - `download-properties` - Download all property rules to JSON files
  - `list-networklists` - List all network lists
  - `download-networklists` - Download all network lists to CSV files
  - `list-clientlists` - List all client lists
  - `download-clientlists` - Download all client lists to CSV files
- **API Client**: Python client with EdgeGrid auth supporting GET/POST/PUT/PATCH/DELETE

## Installation

### Global Tool Install (Recommended)

Install as a global CLI tool:

```bash
uv tool install git+https://github.com/jyflau49/akamai-wrappy
```

Commands are available via the `awp` prefix:

```bash
awp list-properties -k 1-ABCDE:1-12345
awp download-networklists -o ./output
```

**Upgrade:**

```bash
uv tool install --reinstall git+https://github.com/jyflau49/akamai-wrappy
```

### Development Install

Clone and run from source:

```bash
git clone https://github.com/jyflau49/akamai-wrappy.git
cd akamai-wrappy
uv sync
```

Commands are run via `uv run awp`:

```bash
uv run awp list-properties -k 1-ABCDE:1-12345
uv run awp download-networklists -o ./output
```

**Upgrade:**

```bash
git pull && uv sync
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
awp search-asw "Account Name"
```

### search-group

Search for groups by name (case-insensitive partial match):

```bash
awp search-group "Group Name"
awp search-group -k 1-ABCDE:1-12345 "Hong Kong"
```

### list-properties

List all properties with version info:

```bash
awp list-properties
awp list-properties -g grp_123456      # Filter by group ID
awp list-properties -k 1-ABCDE:1-12345 # With account switch key
```

### download-property

Download property rules to JSON:

```bash
awp download-property prp_123456
awp download-property prp_123456 -v 5         # Specific version
awp download-property prp_123456 -o out.json  # Custom output file
```

### download-properties

Download all property rules to JSON files (uses production version if available, otherwise latest):

```bash
awp download-properties
awp download-properties -g grp_123456    # Filter by group ID
awp download-properties -o ./output      # Custom output directory
awp download-properties --delay 30       # Custom delay between downloads
```

> **Note:** Akamai PAPI limits rule tree exports to 3/min. Default delay is 21s to stay within limits. The API client also auto-retries on 429 errors with exponential backoff.

### list-networklists

List all network lists:

```bash
awp list-networklists
awp list-networklists -k 1-ABCDE:1-12345  # With account switch key
```

### download-networklists

Download all network lists to CSV files:

```bash
awp download-networklists
awp download-networklists -o ./output  # Custom output directory
```

### list-clientlists

List all client lists:

```bash
awp list-clientlists
awp list-clientlists -k 1-ABCDE:1-12345  # With account switch key
```

### download-clientlists

Download all client lists to CSV files:

```bash
awp download-clientlists
awp download-clientlists -o ./output  # Custom output directory
```

> **Note:** Network Lists and Client Lists are fetched in a single API call with all elements included.

## Library Usage

```python
from akamai_wrappy import Akamai

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
