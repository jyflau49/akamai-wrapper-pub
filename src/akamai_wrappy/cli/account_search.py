#!/usr/bin/env python
"""Search Akamai account switch keys."""

import argparse
from pprint import pprint
from typing import Any, Dict, List

from tabulate import tabulate

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args


def account_search(akm_api: Akamai, name: str) -> List[Dict[str, Any]]:
    """Search for account switch keys by name.

    Args:
        akm_api: Akamai API client
        name: Search term for account name

    Returns:
        List of matching account switch keys
    """
    result = akm_api.get(
        "/identity-management/v3/api-clients/self/account-switch-keys",
        query=f"search={name}",
    )

    if isinstance(result, (dict, str)):
        pprint(result)
        return []

    return result


def add_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to parser."""
    parser.add_argument(
        "name",
        help="Account name to search (partial match supported)",
    )
    add_common_args(parser)


def run(options: argparse.Namespace) -> None:
    """Run the command with parsed options."""
    akm_api = Akamai.FromOptions(options)
    result = account_search(akm_api, options.name)

    if result:
        print(tabulate(result, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No results found")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search for Akamai account switch keys by name"
    )
    add_args(parser)
    options = parser.parse_args()
    run(options)


if __name__ == "__main__":
    main()
