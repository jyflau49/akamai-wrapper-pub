#!/usr/bin/env python
"""Download Akamai network lists to CSV files."""

import argparse
import csv
import os
import sys
from typing import Any, Dict, List

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args

def download_networklists(
    akm_api: Akamai,
    output_dir: str = "./networklists",
    verbose: bool = False,
) -> None:
    """Download all network lists to CSV files.

    Args:
        akm_api: Akamai API client
        output_dir: Output directory path
        verbose: Enable verbose output
    """
    os.makedirs(output_dir, exist_ok=True)

    if verbose:
        print(f"Output directory: {output_dir}", file=sys.stderr)
        print("Fetching network lists with elements...", file=sys.stderr)

    # Fetch all network lists with elements in one call
    response = akm_api.get(
        "/network-list/v2/network-lists",
        params={"includeElements": "true"},
    )

    if isinstance(response, dict) and "error" in response:
        print(f"Error: {response}", file=sys.stderr)
        return

    network_lists: List[Dict[str, Any]] = response.get("networkLists", [])

    if not network_lists:
        print("No network lists found", file=sys.stderr)
        return

    print(f"Found {len(network_lists)} network lists", file=sys.stderr)
    print("Writing CSV files...", file=sys.stderr)

    success_count = 0

    for i, nl in enumerate(network_lists, 1):
        nl_id = nl.get("uniqueId", "unknown")
        nl_name = nl.get("name", "unknown")
        nl_type = nl.get("type", "IP")
        elements = nl.get("list", []) or []

        # Sanitize filename
        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in nl_name)
        filename = f"{nl_id}_{safe_name}.csv"
        filepath = os.path.join(output_dir, filename)

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["value"])
                for element in elements:
                    writer.writerow([element])

            print(f"✓ {nl_name} ({len(elements)} {nl_type})", file=sys.stderr)
            success_count += 1

        except Exception as e:
            print(f"✗ Failed to write {nl_name}: {e}", file=sys.stderr)

    print(f"\nDownloaded {success_count} of {len(network_lists)} network lists", file=sys.stderr)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Download all Akamai network lists to CSV files"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="./networklists",
        help="Output directory (default: ./networklists)",
    )
    add_common_args(parser)

    options = parser.parse_args()
    akm_api = Akamai.FromOptions(options)

    download_networklists(
        akm_api,
        output_dir=options.output_dir,
        verbose=options.verbose,
    )


if __name__ == "__main__":
    main()
