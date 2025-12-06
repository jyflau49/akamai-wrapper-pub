#!/usr/bin/env python
"""Download Akamai client lists to CSV files."""

import argparse
import csv
import os
import sys
from typing import Any, Dict, List

from akamai_wrappy.api import Akamai
from akamai_wrappy.cli.common import add_common_args

def download_clientlists(
    akm_api: Akamai,
    output_dir: str = "./clientlists",
    verbose: bool = False,
) -> None:
    """Download all client lists to CSV files.

    Args:
        akm_api: Akamai API client
        output_dir: Output directory path
        verbose: Enable verbose output
    """
    os.makedirs(output_dir, exist_ok=True)

    if verbose:
        print(f"Output directory: {output_dir}", file=sys.stderr)
        print("Fetching client lists with items...", file=sys.stderr)

    # Fetch all client lists with items in one call
    response = akm_api.get(
        "/client-list/v1/lists",
        params={"includeItems": "true"},
    )

    if isinstance(response, dict) and "error" in response:
        print(f"Error: {response}", file=sys.stderr)
        return

    client_lists: List[Dict[str, Any]] = response.get("content", [])

    if not client_lists:
        print("No client lists found", file=sys.stderr)
        return

    print(f"Found {len(client_lists)} client lists", file=sys.stderr)
    print("Writing CSV files...", file=sys.stderr)

    success_count = 0

    for i, cl in enumerate(client_lists, 1):
        cl_id = cl.get("listId", "unknown")
        cl_name = cl.get("name", "unknown")
        cl_type = cl.get("type", "")
        staging_status = cl.get("stagingActivationStatus", "")
        prod_status = cl.get("productionActivationStatus", "")
        items = cl.get("items", []) or []

        # Sanitize filename
        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in cl_name)
        filename = f"{cl_id}_{safe_name}.csv"
        filepath = os.path.join(output_dir, filename)

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Header with metadata columns
                writer.writerow([
                    "value",
                    "description",
                    "expirationDate",
                    "tags",
                    "stagingStatus",
                    "productionStatus",
                ])

                for item in items:
                    # Handle item structure - could be dict or string
                    if isinstance(item, dict):
                        value = item.get("value", "")
                        description = item.get("description", "")
                        expiration = item.get("expirationDate", "")
                        tags = ",".join(item.get("tags", []) or [])
                    else:
                        value = str(item)
                        description = ""
                        expiration = ""
                        tags = ""

                    writer.writerow([
                        value,
                        description,
                        expiration,
                        tags,
                        staging_status,
                        prod_status,
                    ])

            print(f"✓ {cl_name} ({len(items)} {cl_type})", file=sys.stderr)
            success_count += 1

        except Exception as e:
            print(f"✗ Failed to write {cl_name}: {e}", file=sys.stderr)

    print(f"\nDownloaded {success_count} of {len(client_lists)} client lists", file=sys.stderr)


def add_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to parser."""
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="./clientlists",
        help="Output directory (default: ./clientlists)",
    )
    add_common_args(parser)


def run(options: argparse.Namespace) -> None:
    """Run the command with parsed options."""
    akm_api = Akamai.FromOptions(options)
    download_clientlists(
        akm_api,
        output_dir=options.output_dir,
        verbose=options.verbose,
    )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Download all Akamai client lists to CSV files"
    )
    add_args(parser)
    options = parser.parse_args()
    run(options)


if __name__ == "__main__":
    main()
