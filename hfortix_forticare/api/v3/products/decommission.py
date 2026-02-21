"""
FortiCare Products - Decommission

Decommission one or more products

API Endpoint:
    post /products/decommission

Decommission products using serial number
Required permission: ReadWrite/Admin

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call decommission endpoint
    >>> response = fcc.api.products.decommission.post(serial_numbers=...)
    >>>
    >>> # Access response data as attributes
    >>> print(response.status)  # 0 for success
    >>> print(response.message)  # Error message (if any)
    >>>
    >>> # Access HTTP metadata
    >>> print(response.http_status_code)  # 200, 404, etc.
    >>> print(response.response_time)  # Request duration
    >>>
    >>> # Get raw response
    >>> raw_dict = response.raw
    >>> dict_copy = response.dict()

Important:
    - Requires OAuth 2.0 Bearer token authentication
    - Rate limits: 100 calls/min, 1000 calls/hour

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, TypedDict, Union

if TYPE_CHECKING:
    from hfortix_core.http.cloud_client import CloudHTTPClient

from hfortix_forticare.models import FortiCareResponse

__all__ = ["ProductDecommission"]


class ProductDecommissionRequest(TypedDict, total=False):
    """ProductDecommissionRequest structure."""

    # Product serial number(s)
    serialNumbers: list

class ProductDecommissionResponse(TypedDict, total=False):
    """ProductDecommissionResponse structure."""

    # OAuth access token
    token: str
    # API version
    version: str
    # API call status code, 0 means success
    status: int
    # Error message in case the request fails, empty message means success
    message: str
    build: str
    error: str


class ProductDecommission:
    """Decommission operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Decommission endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/decommission"
    
    def post(
        self,
        serial_numbers: Union[str, list[str]],
    ) -> FortiCareResponse:
        """
        Decommission one or more products
        
        Decommission products using serial number
Required permission: ReadWrite/Admin
        
        Args:
            serial_numbers: Product serial number(s) (required)
        
        Returns:
            FortiCareResponse object with:
            - Attribute access to all response fields
            - .http_status_code: HTTP status code (200, 404, etc.)
            - .response_time: Request duration in seconds
            - .raw: Full response dictionary
            - .dict(): Convert to plain dict
            
            Response fields:
            - token: OAuth access token
            - version: API version
            - status: API call status code, 0 means success
            - message: Error message in case the request fails, empty message means success
            - error: 
        
        Raises:
            httpx.HTTPStatusError: For HTTP error responses
            httpx.TimeoutException: If request times out
            httpx.RequestError: For network errors
        
        Example:
            >>> response = endpoint.post(serial_numbers=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Normalize serial_numbers to list
        if isinstance(serial_numbers, str):
            serial_numbers = [serial_numbers]

        # Build request body
        request_data = {
            'serialNumbers': serial_numbers,
        }

        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return FortiCareResponse(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
