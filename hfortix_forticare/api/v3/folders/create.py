"""
FortiCare Folders - Create

Creates new asset folder

API Endpoint:
    post /folders/create

Create new asset folder
Required permission: ReadWrite/Admin

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call create endpoint
    >>> response = fcc.api.folders.create.post(folder_name=..., account_id=...)
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

__all__ = ["FolderCreate"]


class FolderCreateRequest(TypedDict, total=False):
    """FolderCreateRequest structure."""

    # Name of new asset folder
    folderName: str
    # Folder's account ID. Optional for API user with Local scope, mandatory
    accountId: int
    # Parent folder id
    parentFolderId: int

class FolderCreateResponse(TypedDict, total=False):
    """FolderCreateResponse structure."""

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

class FolderCreateResponseWithFolders(FortiCareResponse):
    """Specialized response for endpoint with assetFolders."""
    
    @property
    def assetFolders(self):
        """Assetfolders."""
        items = super().__getattribute__("__getattr__")("assetFolders")
        return items[0] if items else None


class FolderCreate:
    """Create operations for folders endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Create endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/folders/create"
    
    def post(
        self,
        folder_name: str,
        account_id: Optional[int] = None,
        parent_folder_id: Optional[int] = None,
    ) -> FolderCreateResponseWithFolders:
        """
        Creates new asset folder
        
        Create new asset folder
Required permission: ReadWrite/Admin
        
        Args:
            folder_name: Name of new asset folder (required)
            account_id: Folder's account ID. Optional for API user with Local scope, mandatory for Org scope. (optional)
            parent_folder_id: Parent folder id (optional)
        
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
            >>> response = endpoint.post(folder_name=..., account_id=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
            'folderName': folder_name,
        }

        if account_id is not None:
            request_data['accountId'] = account_id
        if parent_folder_id is not None:
            request_data['parentFolderId'] = parent_folder_id
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return FolderCreateResponseWithFolders(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
