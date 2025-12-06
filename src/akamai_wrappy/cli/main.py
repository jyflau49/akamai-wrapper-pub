#!/usr/bin/env python
"""Main CLI entry point for akamai-wrappy (awp)."""

import argparse
import sys

from akamai_wrappy.cli import (
    account_search,
    download_clientlists,
    download_networklists,
    group_search,
    list_clientlists,
    list_networklists,
    list_properties,
    properties_download,
    property_download,
)


def main():
    """Main entry point for awp CLI."""
    parser = argparse.ArgumentParser(
        prog="awp",
        description="Akamai Wrappy CLI - Lightweight Akamai utilities",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # search-asw
    search_asw_parser = subparsers.add_parser(
        "search-asw",
        help="Search for account switch keys",
    )
    account_search.add_args(search_asw_parser)

    # search-group
    search_group_parser = subparsers.add_parser(
        "search-group",
        help="Search for groups by name",
    )
    group_search.add_args(search_group_parser)

    # list-properties
    list_props_parser = subparsers.add_parser(
        "list-properties",
        help="List all properties with version info",
    )
    list_properties.add_args(list_props_parser)

    # download-property
    dl_prop_parser = subparsers.add_parser(
        "download-property",
        help="Download property rules to JSON",
    )
    property_download.add_args(dl_prop_parser)

    # download-properties
    dl_props_parser = subparsers.add_parser(
        "download-properties",
        help="Download all property rules to JSON files",
    )
    properties_download.add_args(dl_props_parser)

    # list-networklists
    list_nl_parser = subparsers.add_parser(
        "list-networklists",
        help="List all network lists",
    )
    list_networklists.add_args(list_nl_parser)

    # download-networklists
    dl_nl_parser = subparsers.add_parser(
        "download-networklists",
        help="Download all network lists to CSV files",
    )
    download_networklists.add_args(dl_nl_parser)

    # list-clientlists
    list_cl_parser = subparsers.add_parser(
        "list-clientlists",
        help="List all client lists",
    )
    list_clientlists.add_args(list_cl_parser)

    # download-clientlists
    dl_cl_parser = subparsers.add_parser(
        "download-clientlists",
        help="Download all client lists to CSV files",
    )
    download_clientlists.add_args(dl_cl_parser)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Dispatch to the appropriate run function
    commands = {
        "search-asw": account_search.run,
        "search-group": group_search.run,
        "list-properties": list_properties.run,
        "download-property": property_download.run,
        "download-properties": properties_download.run,
        "list-networklists": list_networklists.run,
        "download-networklists": download_networklists.run,
        "list-clientlists": list_clientlists.run,
        "download-clientlists": download_clientlists.run,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
