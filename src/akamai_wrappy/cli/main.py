#!/usr/bin/env python
"""Main CLI entry point for akamai-wrappy (awp)."""

import argparse
import sys

from rich.console import Console
from rich.table import Table
from rich.text import Text

from akamai_wrappy import __version__
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

COMMANDS = {
    "search-asw": (account_search, "Search for account switch keys"),
    "search-group": (group_search, "Search for groups by name"),
    "list-properties": (list_properties, "List all properties with version info"),
    "download-property": (property_download, "Download property rules to JSON"),
    "download-properties": (properties_download, "Download all property rules to JSON"),
    "list-networklists": (list_networklists, "List all network lists"),
    "download-networklists": (download_networklists, "Download network lists to CSV"),
    "list-clientlists": (list_clientlists, "List all client lists"),
    "download-clientlists": (download_clientlists, "Download client lists to CSV"),
}


def print_help():
    """Print custom colored help message."""
    console = Console()

    # Header
    header = Text()
    header.append("awp", style="bold cyan")
    header.append(": Akamai Wrappy CLI - Lightweight Akamai utilities\n", style="dim")
    console.print(header)

    # Usage
    console.print("[bold]Usage:[/bold] awp [OPTIONS] <COMMAND>\n")

    # Commands table
    console.print("[bold]Commands:[/bold]")
    table = Table(show_header=False, box=None, padding=(0, 2, 0, 2))
    table.add_column(style="green")
    table.add_column(style="dim")

    for cmd, (_, desc) in COMMANDS.items():
        table.add_row(cmd, desc)

    console.print(table)
    console.print()

    # Options
    console.print("[bold]Options:[/bold]")
    console.print("  [green]-h, --help[/green]     Print help")
    console.print("  [green]-V, --version[/green]  Print version")
    console.print()

    # Global options
    console.print("[bold]Global options:[/bold] [dim](available for all commands)[/dim]")
    console.print("  [green]-k, --account-switch-key[/green]  Account switch key for multi-account access")
    console.print("  [green]-t, --timeout[/green]             Request timeout in seconds (default: 30)")
    console.print("  [green]--edgerc[/green]                  Path to .edgerc file (default: ~/.edgerc)")
    console.print("  [green]--section[/green]                 Section in .edgerc (default: default)")
    console.print("  [green]--verbose[/green]                 Enable verbose output")
    console.print()

    # Footer
    console.print("[dim]For help with a specific command: awp <command> --help[/dim]")


def print_version():
    """Print version."""
    console = Console()
    console.print(f"[bold cyan]awp[/bold cyan] {__version__}")


def main():
    """Main entry point for awp CLI."""
    # Handle --help and --version before argparse
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    if sys.argv[1] in ("-V", "--version"):
        print_version()
        sys.exit(0)

    # Build parser for subcommands
    parser = argparse.ArgumentParser(
        prog="awp",
        add_help=False,
    )
    subparsers = parser.add_subparsers(dest="command")

    for cmd, (module, desc) in COMMANDS.items():
        sub = subparsers.add_parser(cmd, help=desc)
        module.add_args(sub)

    args = parser.parse_args()

    if args.command is None:
        print_help()
        sys.exit(1)

    # Dispatch
    COMMANDS[args.command][0].run(args)


if __name__ == "__main__":
    main()
