"""Common CLI utilities and argument helpers."""

import argparse


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to an argument parser.

    Args:
        parser: ArgumentParser to add arguments to
    """
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
        help="Request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--edgerc",
        type=str,
        default="~/.edgerc",
        help="Path to .edgerc credentials file (default: ~/.edgerc)",
    )
    parser.add_argument(
        "--section",
        type=str,
        default="default",
        help="Section in .edgerc file (default: default)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
