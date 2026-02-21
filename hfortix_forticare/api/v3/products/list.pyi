"""Type stubs for FortiCare Products - List"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, Asset

class ProductListRequest(TypedDict, total=False):
    """ProductListRequest structure."""

    # Serial number or serial number search pattern
    serialNumber: str
    # Date time in ISO 8601 format. Return products with entitlement expirin
    expireBefore: str
    # Allowed values are Registered and Pending. Default value is Registered
    status: str
    # Product model name (optional)
    productModel: str
    # Optional parameter for API user with Local scope, mandatory for Org sc
    accountId: int

class ProductListResponse(TypedDict, total=False):
    """ProductListResponse structure."""

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

class ProductListResponseWithAssets(FortiCareResponse):
    """Specialized response for endpoint with assets."""
    
    @property
    def assets(self) -> FortiCareList[Asset]:
        """Assets."""
        ...

class ProductList:
    """List operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        account_id: Optional[int] = None,
        expire_before: Optional[str] = None,
        product_model: Optional[str] = None,
        serial_number: Optional[str] = "%",
        status: Optional[str] = None,
    ) -> ProductListResponseWithAssets: ...

