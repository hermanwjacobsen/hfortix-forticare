"""Type stubs for FortiCare Products - Folder"""

from typing import Any, Optional, TypedDict, Union
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse

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
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        folder_id: Optional[int],
        serial_numbers: Union[str, list[str]],
    ) -> FortiCareResponse: ...

