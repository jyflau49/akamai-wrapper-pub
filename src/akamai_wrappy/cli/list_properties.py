#!/usr/bin/env python
"""List Akamai properties."""

import argparse
import sys
import time
from typing import Any, Dict, List

from tabulate import tabulate

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args


def list_properties(
    akm_api: Akamai,
    group_filter: str | None = None,
    rate_limit_delay: float = 0.3,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """List all properties across all groups.

    Args:
        akm_api: Akamai API client
        group_filter: Optional group ID filter (e.g., grp_123456)
        rate_limit_delay: Delay between API calls in seconds
        verbose: Enable verbose output

    Returns:
        List of properties with key info
    """
    if verbose:
        print("Fetching groups...", file=sys.stderr)

    groups_response = akm_api.get("/papi/v1/groups")

    if isinstance(groups_response, dict) and "error" in groups_response:
        print(f"Error: {groups_response}", file=sys.stderr)
        return []

    groups = groups_response.get("groups", {}).get("items", [])
    if verbose:
        print(f"Found {len(groups)} groups", file=sys.stderr)

    properties_list = []

    for group in groups:
        group_id = group.get("groupId")
        group_name = group.get("groupName", "Unknown")
        contract_ids = group.get("contractIds", [])

        if not contract_ids:
            continue

        # Filter by group ID if specified
        if group_filter and group_filter != group_id:
            continue

        for contract_id in contract_ids:
            if verbose:
                print(f"Fetching: {group_name} ({group_id})", file=sys.stderr)

            time.sleep(rate_limit_delay)

            props_response = akm_api.get(
                "/papi/v1/properties",
                params={"contractId": contract_id, "groupId": group_id},
            )

            if isinstance(props_response, dict) and "error" in props_response:
                print(f"Warning: {props_response}", file=sys.stderr)
                continue

            properties = props_response.get("properties", {}).get("items", [])

            for prop in properties:
                properties_list.append(
                    {
                        "propertyId": prop.get("propertyId"),
                        "propertyName": prop.get("propertyName"),
                        "prodVer": prop.get("productionVersion"),
                        "stgVer": prop.get("stagingVersion"),
                        "latestVer": prop.get("latestVersion"),
                        "groupId": group_id,
                    }
                )

    return properties_list


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="List all Akamai properties with version info"
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        default=None,
        help="Filter by group ID (e.g., grp_123456)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="Delay between API calls in seconds (default: 0.3)",
    )
    add_common_args(parser)

    options = parser.parse_args()
    akm_api = Akamai.FromOptions(options)
    result = list_properties(
        akm_api,
        group_filter=options.group,
        rate_limit_delay=options.delay,
        verbose=options.verbose,
    )

    if result:
        print(tabulate(result, headers="keys", tablefmt="fancy_grid"))
        print(f"\nTotal: {len(result)} properties")
    else:
        print("No properties found")


if __name__ == "__main__":
    main()
