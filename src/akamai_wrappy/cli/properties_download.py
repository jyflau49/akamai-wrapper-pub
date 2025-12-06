#!/usr/bin/env python
"""Download all Akamai property rules to JSON files."""

import argparse
import json
import os
import sys
import time

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args


def download_property_rules(
    akm_api: Akamai,
    property_id: str,
    property_name: str,
    version: int,
    contract_id: str,
    group_id: str,
    output_dir: str,
) -> bool:
    """Download a single property's rule tree.

    Args:
        akm_api: Akamai API client
        property_id: Property ID
        property_name: Property name
        version: Property version
        contract_id: Contract ID
        group_id: Group ID
        output_dir: Output directory path

    Returns:
        True if successful, False otherwise
    """
    try:
        # Fetch the rule tree
        rules_response = akm_api.get(
            f"/papi/v1/properties/{property_id}/versions/{version}/rules",
            params={"contractId": contract_id, "groupId": group_id},
        )

        if isinstance(rules_response, dict) and "error" in rules_response:
            print(f"Error downloading {property_name}: {rules_response}", file=sys.stderr)
            return False

        # Determine output filename
        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in property_name)
        output_file = os.path.join(output_dir, f"{safe_name}_v{version}.json")

        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rules_response, f, indent=2)

        print(f"✓ {property_name} v{version}", file=sys.stderr)
        return True

    except Exception as e:
        print(f"✗ Failed to download {property_name}: {e}", file=sys.stderr)
        return False


# Akamai PAPI rate limit: 3 rule tree exports per minute
DEFAULT_EXPORT_DELAY = 21  # seconds (safe for 3/min limit)


def download_properties(
    akm_api: Akamai,
    group_filter: str | None = None,
    output_dir: str = "./properties",
    rate_limit_delay: float = DEFAULT_EXPORT_DELAY,
    verbose: bool = False,
) -> None:
    """Download all property rule trees to JSON files.

    Args:
        akm_api: Akamai API client
        group_filter: Optional group ID filter
        output_dir: Output directory path
        rate_limit_delay: Delay between downloads in seconds (default: 21s for rate limit)
        verbose: Enable verbose output
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    if verbose:
        print(f"Output directory: {output_dir}", file=sys.stderr)

    # Get groups and properties directly to have access to contract info
    if verbose:
        print("Fetching groups...", file=sys.stderr)

    groups_response = akm_api.get("/papi/v1/groups")
    if isinstance(groups_response, dict) and "error" in groups_response:
        print(f"Error: {groups_response}", file=sys.stderr)
        return

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
                        "latestVer": prop.get("latestVersion"),
                        "groupId": group_id,
                        "contractId": contract_id,
                    }
                )

    if not properties_list:
        print("No properties found", file=sys.stderr)
        return

    print(f"Found {len(properties_list)} properties", file=sys.stderr)
    print("Starting downloads...", file=sys.stderr)

    success_count = 0
    total_count = len(properties_list)

    for i, prop in enumerate(properties_list, 1):
        property_id = prop.get("propertyId")
        property_name = prop.get("propertyName")
        version = prop.get("prodVer") or prop.get("latestVer")
        contract_id = prop.get("contractId")
        group_id = prop.get("groupId")

        if not all([property_id, property_name, version, contract_id, group_id]):
            print(f"✗ Skipping incomplete property data: {prop}", file=sys.stderr)
            continue

        if verbose:
            print(f"[{i}/{total_count}] {property_name}...", file=sys.stderr)

        # Rate limiting
        if i > 1:
            time.sleep(rate_limit_delay)

        if download_property_rules(
            akm_api,
            property_id,
            property_name,
            version,
            contract_id,
            group_id,
            output_dir,
        ):
            success_count += 1

    print(f"\nDownloaded {success_count} of {total_count} properties", file=sys.stderr)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Download all Akamai property rules to JSON files"
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        default=None,
        help="Filter by group ID (e.g., grp_123456)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="./properties",
        help="Output directory (default: ./properties)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_EXPORT_DELAY,
        help=f"Delay between downloads in seconds (default: {DEFAULT_EXPORT_DELAY}, for 3/min rate limit)",
    )
    add_common_args(parser)

    options = parser.parse_args()
    akm_api = Akamai.FromOptions(options)

    download_properties(
        akm_api,
        group_filter=options.group,
        output_dir=options.output_dir,
        rate_limit_delay=options.delay,
        verbose=options.verbose,
    )


if __name__ == "__main__":
    main()
