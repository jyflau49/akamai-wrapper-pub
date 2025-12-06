#!/usr/bin/env python
"""List Akamai client lists."""

import argparse
import sys
from typing import Any, Dict, List

from tabulate import tabulate

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args, get_table_format


def list_clientlists(
    akm_api: Akamai,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """List all client lists.

    Args:
        akm_api: Akamai API client
        verbose: Enable verbose output

    Returns:
        List of client list metadata dicts
    """
    if verbose:
        print("Fetching client lists...", file=sys.stderr)

    response = akm_api.get("/client-list/v1/lists")

    if isinstance(response, dict) and "error" in response:
        print(f"Error: {response}", file=sys.stderr)
        return []

    # Extract client lists from response
    client_lists = response.get("content", [])

    if verbose:
        print(f"Found {len(client_lists)} client lists", file=sys.stderr)

    results = []
    for cl in client_lists:
        results.append({
            "name": cl.get("name", ""),
            "listId": cl.get("listId", ""),
            "type": cl.get("type", ""),
            "itemsCount": cl.get("itemsCount", 0),
            "stagingStatus": cl.get("stagingActivationStatus", ""),
            "productionStatus": cl.get("productionActivationStatus", ""),
        })

    return results


def add_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to parser."""
    add_common_args(parser)


def run(options: argparse.Namespace) -> None:
    """Run the command with parsed options."""
    akm_api = Akamai.FromOptions(options)
    results = list_clientlists(akm_api, verbose=options.verbose)

    if not results:
        print("No client lists found", file=sys.stderr)
        sys.exit(1)

    print(tabulate(results, headers="keys", tablefmt=get_table_format(options)))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="List all Akamai client lists"
    )
    add_args(parser)
    options = parser.parse_args()
    run(options)


if __name__ == "__main__":
    main()
