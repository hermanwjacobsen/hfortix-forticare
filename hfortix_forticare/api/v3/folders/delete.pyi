"""Type stubs for FortiCare Folders - Delete"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse

class FolderDeleteRequest(TypedDict, total=False):
    """FolderDeleteRequest structure."""

    # Asset folder id
    folderId: int
    # Folder's account ID. Optional for API user with Local scope, mandatory
    accountId: int

class FolderDeleteResponse(TypedDict, total=False):
    """FolderDeleteResponse structure."""

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

class FolderDelete:
    """Delete operations for folders endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        folder_id: Optional[int],
        account_id: Optional[int] = None,
    ) -> FortiCareResponse: ...

