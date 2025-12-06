#!/bin/bash
# Smoke test for akamai-wrappy CLI
# Run: ./scripts/smoke_test.sh
# Requires: valid ~/.edgerc credentials

set -e

echo "=== akamai-wrappy Smoke Test ==="
echo ""

# Check if running via uv run or global install
if command -v awp &> /dev/null; then
    AWP="awp"
    echo "Using global install: awp"
else
    AWP="uv run awp"
    echo "Using dev install: uv run awp"
fi

echo ""
echo "--- Testing --help for all commands ---"

$AWP --help > /dev/null && echo "✓ awp --help"
$AWP search-asw --help > /dev/null && echo "✓ awp search-asw --help"
$AWP search-group --help > /dev/null && echo "✓ awp search-group --help"
$AWP list-properties --help > /dev/null && echo "✓ awp list-properties --help"
$AWP download-property --help > /dev/null && echo "✓ awp download-property --help"
$AWP download-properties --help > /dev/null && echo "✓ awp download-properties --help"
$AWP list-networklists --help > /dev/null && echo "✓ awp list-networklists --help"
$AWP download-networklists --help > /dev/null && echo "✓ awp download-networklists --help"
$AWP list-clientlists --help > /dev/null && echo "✓ awp list-clientlists --help"
$AWP download-clientlists --help > /dev/null && echo "✓ awp download-clientlists --help"

echo ""
echo "--- Testing Python import ---"

uv run python -c "from akamai_wrappy import Akamai, __version__; print(f'✓ Import OK, version: {__version__}')"

echo ""
echo "--- Testing API connectivity (requires valid .edgerc) ---"

# Optional: test actual API calls if credentials exist
if [ -f ~/.edgerc ]; then
    echo "Found ~/.edgerc, testing API calls..."
    
    # Test search-asw (should return results or empty)
    if $AWP search-asw "test" > /dev/null 2>&1; then
        echo "✓ awp search-asw (API call)"
    else
        echo "⚠ awp search-asw (API call failed, check credentials)"
    fi
else
    echo "⚠ No ~/.edgerc found, skipping API tests"
fi

echo ""
echo "=== Smoke Test Complete ==="
