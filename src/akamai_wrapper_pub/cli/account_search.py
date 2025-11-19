#!/usr/bin/env python
"""Search Akamai account switch keys."""

import argparse
import logging
import sys
from pprint import pprint
from typing import List, Dict, Any

from tabulate import tabulate

from akamai_wrapper_pub.api import Akamai

logger = logging.getLogger("akamai-account-search")


def account_search(akm_api: Akamai, name: str) -> List[Dict[str, Any]]:
    """Search for account switch keys by name.
    
    Args:
        akm_api: Akamai API client
        name: Search term for account name
        
    Returns:
        List of matching account switch keys
    """
    result = akm_api.get(
        '/identity-management/v3/api-clients/self/account-switch-keys',
        query=f'search={name}'
    )
    
    if isinstance(result, (dict, str)):
        pprint(result)
        return []
    
    return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search Akamai account switch keys"
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds'
    )
    parser.add_argument(
        'names',
        nargs=argparse.REMAINDER,
        help='Account names to search'
    )
    parser.add_argument(
        '--edgerc',
        type=str,
        default="~/.edgerc",
        help='Location of the credentials file'
    )
    parser.add_argument(
        '--section',
        type=str,
        default="default",
        help='Section of the credentials file'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    options = parser.parse_args()
    
    if options.verbose:
        logger.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        logger.addHandler(stdout_handler)
    
    if not options.names:
        parser.error("Please provide at least one account name to search")
    
    akm_api = Akamai.FromOptions(options)
    result = account_search(akm_api, options.names[0])
    
    if result:
        print(tabulate(result, headers='keys', tablefmt="fancy_grid"))
    else:
        print("No results found")


if __name__ == '__main__':
    main()
