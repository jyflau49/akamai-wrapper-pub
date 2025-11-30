#!/usr/bin/env python
"""Search Akamai groups."""

import argparse
import logging
import sys
from pprint import pprint
from typing import Any, Dict, List

from tabulate import tabulate

from akamai_wrapper_pub.api import Akamai

logger = logging.getLogger("akamai-group-search")


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


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Search Akamai groups")
    parser.add_argument(
        "name",
        help="Group name to search (case-insensitive substring match)",
    )
    parser.add_argument(
        "-k",
        "--account-switch-key",
        type=str,
        default=None,
        dest="accountSwitchKey",
        help="Account switch key for multi-account access",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds",
    )
    parser.add_argument(
        "--edgerc",
        type=str,
        default="~/.edgerc",
        help="Location of the credentials file",
    )
    parser.add_argument(
        "--section",
        type=str,
        default="default",
        help="Section of the credentials file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    options = parser.parse_args()

    if options.verbose:
        logger.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        logger.addHandler(stdout_handler)

    akm_api = Akamai.FromOptions(options)
    result = group_search(akm_api, options.name)

    if result:
        print(tabulate(result, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No results found")


if __name__ == "__main__":
    main()
