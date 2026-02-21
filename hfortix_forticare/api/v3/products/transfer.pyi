"""Type stubs for FortiCare Products - Transfer"""

from typing import Any, Optional, TypedDict, Union
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, Asset

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
    def assets(self) -> FortiCareList[Asset]:
        """Assets."""
        ...

class ProductTransfer:
    """Transfer operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        serial_numbers: Optional[Union[str, list[str]]] = None,
        source_account_id: Optional[int] = None,
        target_account_id: Optional[int] = None,
    ) -> ProductTransferResponseWithAssets: ...

