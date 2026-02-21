"""
FortiCare Products - Folder

Update folder of a product

API Endpoint:
    post /products/folder

Move product to an asset folder.To use My Assets folder as target, send folderId = null.
Required permission: ReadWrite/Admin

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call folder endpoint
    >>> response = fcc.api.products.folder.post(folder_id=..., serial_numbers=...)
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

__all__ = ["ProductFolder"]


class ProductFolderRequest(TypedDict, total=False):
    """ProductFolderRequest structure."""

    # Target asset folder id
    folderId: int
    # Serial numbers to move
    serialNumbers: list

class ProductFolderResponse(TypedDict, total=False):
    """ProductFolderResponse structure."""

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


class ProductFolder:
    """Folder operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Folder endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/folder"
    
    def post(
        self,
        folder_id: Optional[int],
        serial_numbers: Union[str, list[str]],
    ) -> FortiCareResponse:
        """
        Update folder of a product
        
        Move product to an asset folder.To use My Assets folder as target, send folderId = null.
Required permission: ReadWrite/Admin
        
        Args:
            folder_id: Target asset folder id (required)
            serial_numbers: Serial numbers to move (required)
        
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
            >>> response = endpoint.post(folder_id=..., serial_numbers=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Normalize serial_numbers to list
        if isinstance(serial_numbers, str):
            serial_numbers = [serial_numbers]

        # Build request body
        request_data = {
            'folderId': folder_id,
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
