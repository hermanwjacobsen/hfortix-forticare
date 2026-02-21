"""
FortiCare Products - Transfer

Transfers products between accounts in the same Organization

API Endpoint:
    post /products/transfer

The API user making this request should have access to source and target accounts through OU scope
Required permission: ReadWrite/Admin

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call transfer endpoint
    >>> response = fcc.api.products.transfer.post(source_account_id=..., target_account_id=...)
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

__all__ = ["ProductTransfer"]


class ProductTransferRequest(TypedDict, total=False):
    """ProductTransferRequest structure."""

    # Source account id
    sourceAccountId: int
    # Target account id
    targetAccountId: int
    # Serial numbers to transfer
    serialNumbers: list

class ProductTransferResponse(TypedDict, total=False):
    """ProductTransferResponse structure."""

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
    assets: list[any]

class ProductTransferResponseWithAssets(FortiCareResponse):
    """Specialized response for endpoint with assets."""
    
    @property
    def assets(self):
        """Assets."""
        return super().__getattribute__("__getattr__")("assets")


class ProductTransfer:
    """Transfer operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Transfer endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/transfer"
    
    def post(
        self,
        serial_numbers: Optional[Union[str, list[str]]] = None,
        source_account_id: Optional[int] = None,
        target_account_id: Optional[int] = None,
    ) -> ProductTransferResponseWithAssets:
        """
        Transfers products between accounts in the same Organization
        
        The API user making this request should have access to source and target accounts through OU scope
Required permission: ReadWrite/Admin
        
        Args:
            source_account_id: Source account id (optional)
            target_account_id: Target account id (optional)
            serial_numbers: Serial numbers to transfer (optional)
        
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
            >>> response = endpoint.post(source_account_id=..., target_account_id=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Normalize serial_numbers to list
        if isinstance(serial_numbers, str):
            serial_numbers = [serial_numbers]

        # Build request body
        request_data = {
        }

        if source_account_id is not None:
            request_data['sourceAccountId'] = source_account_id
        if target_account_id is not None:
            request_data['targetAccountId'] = target_account_id
        if serial_numbers is not None:
            request_data['serialNumbers'] = serial_numbers
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return ProductTransferResponseWithAssets(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
