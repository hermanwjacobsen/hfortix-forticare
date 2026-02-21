"""Type stubs for FortiCare Folders - List"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, Folder

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
    def assetFolders(self) -> FortiCareList[Folder]:
        """Assetfolders."""
        ...

class FolderList:
    """List operations for folders endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        account_id: Optional[int] = None,
    ) -> FolderListResponseWithFolders: ...

