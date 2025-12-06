#!/usr/bin/env python
"""List Akamai network lists."""

import argparse
import sys
from typing import Any, Dict, List

from tabulate import tabulate

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args, get_table_format


def list_networklists(
    akm_api: Akamai,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """List all network lists.

    Args:
        akm_api: Akamai API client
        verbose: Enable verbose output

    Returns:
        List of network list metadata dicts
    """
    if verbose:
        print("Fetching network lists...", file=sys.stderr)

    response = akm_api.get("/network-list/v2/network-lists")

    if isinstance(response, dict) and "error" in response:
        print(f"Error: {response}", file=sys.stderr)
        return []

    # Extract network lists from response
    network_lists = response.get("networkLists", [])

    if verbose:
        print(f"Found {len(network_lists)} network lists", file=sys.stderr)

    results = []
    for nl in network_lists:
        results.append({
            "name": nl.get("name", ""),
            "uniqueId": nl.get("uniqueId", ""),
            "type": nl.get("type", ""),
            "elementCount": nl.get("elementCount", 0),
        })

    return results


def add_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to parser."""
    add_common_args(parser)


def run(options: argparse.Namespace) -> None:
    """Run the command with parsed options."""
    akm_api = Akamai.FromOptions(options)
    results = list_networklists(akm_api, verbose=options.verbose)

    if not results:
        print("No network lists found", file=sys.stderr)
        sys.exit(1)

    print(tabulate(results, headers="keys", tablefmt=get_table_format(options)))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="List all Akamai network lists"
    )
    add_args(parser)
    options = parser.parse_args()
    run(options)


if __name__ == "__main__":
    main()
