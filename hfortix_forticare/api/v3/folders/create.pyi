"""Type stubs for FortiCare Folders - Create"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, Folder

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
    def assetFolders(self) -> Folder:
        """Assetfolders."""
        ...

class FolderCreate:
    """Create operations for folders endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        folder_name: str,
        account_id: Optional[int] = None,
        parent_folder_id: Optional[int] = None,
    ) -> FolderCreateResponseWithFolders: ...

