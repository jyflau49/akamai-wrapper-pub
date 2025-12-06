#!/usr/bin/env python
"""Download Akamai property rules."""

import argparse
import json
import sys

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args


def property_download(
    akm_api: Akamai,
    property_id: str,
    version: int | None = None,
    output_file: str | None = None,
) -> None:
    """Download property rules to JSON file.

    Args:
        akm_api: Akamai API client
        property_id: Property ID (e.g., prp_123456)
        version: Specific version to download (default: production or latest)
        output_file: Output file path (default: {propertyName}_v{version}.json)
    """
    print(f"Fetching property info for {property_id}...", file=sys.stderr)
    prop_response = akm_api.get(f"/papi/v1/properties/{property_id}")

    if isinstance(prop_response, dict) and "error" in prop_response:
        print(f"Error: {prop_response}", file=sys.stderr)
        return

    properties = prop_response.get("properties", {}).get("items", [])
    if not properties:
        print(f"Property {property_id} not found", file=sys.stderr)
        return

    prop = properties[0]
    contract_id = prop.get("contractId")
    group_id = prop.get("groupId")
    property_name = prop.get("propertyName")

    # Determine version to download
    if version is None:
        version = prop.get("productionVersion") or prop.get("latestVersion")
        if not version:
            print("No version found for this property", file=sys.stderr)
            return
        print(f"Using version: {version} (production or latest)", file=sys.stderr)

    # Fetch the rule tree
    print(f"Downloading rules for {property_name} v{version}...", file=sys.stderr)
    rules_response = akm_api.get(
        f"/papi/v1/properties/{property_id}/versions/{version}/rules",
        params={"contractId": contract_id, "groupId": group_id},
    )

    if isinstance(rules_response, dict) and "error" in rules_response:
        print(f"Error: {rules_response}", file=sys.stderr)
        return

    # Determine output filename
    if output_file is None:
        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in property_name)
        output_file = f"{safe_name}_v{version}.json"

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rules_response, f, indent=2)

    print(f"Saved to {output_file}")


def add_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to parser."""
    parser.add_argument(
        "property_id",
        help="Property ID (e.g., prp_123456)",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=int,
        default=None,
        help="Version to download (default: production or latest)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (default: {propertyName}_v{version}.json)",
    )
    add_common_args(parser)


def run(options: argparse.Namespace) -> None:
    """Run the command with parsed options."""
    akm_api = Akamai.FromOptions(options)
    property_download(
        akm_api,
        property_id=options.property_id,
        version=options.version,
        output_file=options.output,
    )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Download Akamai property rules to JSON file"
    )
    add_args(parser)
    options = parser.parse_args()
    run(options)


if __name__ == "__main__":
    main()
