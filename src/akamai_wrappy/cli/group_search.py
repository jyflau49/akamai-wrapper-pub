#!/usr/bin/env python
"""Search Akamai groups."""

import argparse
from pprint import pprint
from typing import Any, Dict, List

from tabulate import tabulate

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args


def group_search(akm_api: Akamai, name: str) -> List[Dict[str, Any]]:
    """Search for groups by name.

    Args:
        akm_api: Akamai API client
        name: Search term for group name (case-insensitive substring match)

    Returns:
        List of matching groups
    """
    result = akm_api.get("/papi/v1/groups")

    if isinstance(result, dict) and "error" in result:
        pprint(result)
        return []

    groups = result.get("groups", {}).get("items", [])

    # Filter by name (case-insensitive substring match)
    search_lower = name.lower()
    matches = []
    for group in groups:
        group_name = group.get("groupName", "")
        if search_lower in group_name.lower():
            matches.append(
                {
                    "groupId": group.get("groupId"),
                    "groupName": group_name,
                    "contractIds": ";".join(group.get("contractIds", [])),
                }
            )

    return matches


def add_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to parser."""
    parser.add_argument(
        "name",
        help="Group name to search",
    )
    add_common_args(parser)


def run(options: argparse.Namespace) -> None:
    """Run the command with parsed options."""
    akm_api = Akamai.FromOptions(options)
    result = group_search(akm_api, options.name)

    if result:
        print(tabulate(result, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No results found")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search for Akamai groups by name (case-insensitive partial match)"
    )
    add_args(parser)
    options = parser.parse_args()
    run(options)


if __name__ == "__main__":
    main()
