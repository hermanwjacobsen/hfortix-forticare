"""
FortiCare Folders - List

Returns asset folder list

API Endpoint:
    post /folders/list

Query folder list
Required permission: Read

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call list endpoint
    >>> response = fcc.api.folders.list.post(account_id=...)
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

from typing import TYPE_CHECKING, Any, Optional, TypedDict

if TYPE_CHECKING:
    from hfortix_core.http.cloud_client import CloudHTTPClient

from hfortix_forticare.models import FortiCareResponse

__all__ = ["FolderList"]


class FolderListRequest(TypedDict, total=False):
    """FolderListRequest structure."""

    # Folders account ID. Optional for API user with Local scope, mandatory 
    accountId: int

class FolderListResponse(TypedDict, total=False):
    """FolderListResponse structure."""

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
    assetFolders: list[any]

class FolderListResponseWithFolders(FortiCareResponse):
    """Specialized response for endpoint with assetFolders."""
    
    @property
    def assetFolders(self):
        """Assetfolders."""
        return super().__getattribute__("__getattr__")("assetFolders")


class FolderList:
    """List operations for folders endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize List endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/folders/list"
    
    def post(
        self,
        account_id: Optional[int] = None,
    ) -> FolderListResponseWithFolders:
        """
        Returns asset folder list
        
        Query folder list
Required permission: Read
        
        Args:
            account_id: Folders account ID. Optional for API user with Local scope, mandatory for Org scope. (optional)
        
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
            >>> response = endpoint.post(account_id=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
        }

        if account_id is not None:
            request_data['accountId'] = account_id
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return FolderListResponseWithFolders(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
