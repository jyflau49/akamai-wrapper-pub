"""Akamai API client base class."""

import os
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc


class Akamai:
    """Base Akamai API client with EdgeGrid authentication."""

    def __init__(
        self,
        edgerc_path: str = "~/.edgerc",
        section: str = "default",
        timeout: int = 30,
        account_switch_key: Optional[str] = None,
    ):
        """Initialize Akamai API client.

        Args:
            edgerc_path: Path to .edgerc file
            section: Section name in .edgerc
            timeout: Request timeout in seconds
            account_switch_key: Optional account switch key
        """
        self.timeout = timeout
        self.account_switch_key = account_switch_key

        # Load EdgeGrid credentials
        edgerc_path = os.path.expanduser(edgerc_path)
        edgerc = EdgeRc(edgerc_path)
        self.base_url = f"https://{edgerc.get(section, 'host')}"

        # Create session with EdgeGrid auth
        self.session = requests.Session()
        self.session.auth = EdgeGridAuth.from_edgerc(edgerc, section)

    @classmethod
    def FromOptions(cls, options):
        """Create Akamai client from argparse options.

        Args:
            options: argparse Namespace with edgerc, section, timeout attributes

        Returns:
            Akamai: Configured API client
        """
        return cls(
            edgerc_path=getattr(options, "edgerc", "~/.edgerc"),
            section=getattr(options, "section", "default"),
            timeout=getattr(options, "timeout", 30),
            account_switch_key=getattr(options, "accountSwitchKey", None),
        )

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response and extract JSON or error.

        Args:
            response: requests Response object

        Returns:
            Parsed JSON response or error dict
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except ValueError as e:
            return {"error": f"JSON decode error: {e}"}

    def get(
        self,
        path: str,
        query: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make GET request to Akamai API.

        Args:
            path: API path (e.g., '/identity-management/v3/...')
            query: Optional query string
            params: Optional query parameters dict
            headers: Optional request headers

        Returns:
            Parsed JSON response or error dict/string
        """
        url = urljoin(self.base_url, path)

        # Build query parameters
        query_params = params or {}
        if query:
            # Handle query string format
            if "=" in query:
                for pair in query.split("&"):
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        query_params[key] = value
            else:
                query_params["search"] = query

        if self.account_switch_key:
            query_params["accountSwitchKey"] = self.account_switch_key

        response = self.session.get(
            url, params=query_params, headers=headers, timeout=self.timeout
        )
        return self._handle_response(response)

    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make PUT request to Akamai API.

        Args:
            path: API path
            data: Request body data
            params: Optional query parameters
            headers: Optional request headers

        Returns:
            Parsed JSON response or error dict/string
        """
        url = urljoin(self.base_url, path)

        query_params = params or {}
        if self.account_switch_key:
            query_params["accountSwitchKey"] = self.account_switch_key

        response = self.session.put(
            url, json=data, params=query_params, headers=headers, timeout=self.timeout
        )
        return self._handle_response(response)

    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make POST request to Akamai API.

        Args:
            path: API path
            data: Request body data
            params: Optional query parameters
            headers: Optional request headers

        Returns:
            Parsed JSON response or error dict/string
        """
        url = urljoin(self.base_url, path)

        query_params = params or {}
        if self.account_switch_key:
            query_params["accountSwitchKey"] = self.account_switch_key

        response = self.session.post(
            url, json=data, params=query_params, headers=headers, timeout=self.timeout
        )
        return self._handle_response(response)

    def patch(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make PATCH request to Akamai API.

        Args:
            path: API path
            data: Request body data
            params: Optional query parameters
            headers: Optional request headers

        Returns:
            Parsed JSON response or error dict/string
        """
        url = urljoin(self.base_url, path)

        query_params = params or {}
        if self.account_switch_key:
            query_params["accountSwitchKey"] = self.account_switch_key

        response = self.session.patch(
            url, json=data, params=query_params, headers=headers, timeout=self.timeout
        )
        return self._handle_response(response)

    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make DELETE request to Akamai API.

        Args:
            path: API path
            params: Optional query parameters
            headers: Optional request headers

        Returns:
            Parsed JSON response or error dict/string
        """
        url = urljoin(self.base_url, path)

        query_params = params or {}
        if self.account_switch_key:
            query_params["accountSwitchKey"] = self.account_switch_key

        response = self.session.delete(
            url, params=query_params, headers=headers, timeout=self.timeout
        )
        return self._handle_response(response)
