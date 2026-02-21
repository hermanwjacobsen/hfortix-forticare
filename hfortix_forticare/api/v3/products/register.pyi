"""Type stubs for FortiCare Products - Register"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, Asset

class ProductRegisterRequest(TypedDict, total=False):
    """ProductRegisterRequest structure."""

    # Product's Account ID. Optional for API user with Local scope, mandator
    accountId: int
    registrationUnits: list[object]
    locations: list[object]

class ProductRegisterResponse(TypedDict, total=False):
    """ProductRegisterResponse structure."""

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

class ProductRegisterResponseWithAssets(FortiCareResponse):
    """Specialized response for endpoint with assets."""
    
    @property
    def assets(self) -> Asset:
        """Assets."""
        ...

class ProductRegister:
    """Register operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        account_id: Optional[int] = None,
        locations: Optional[list[object]] = None,
        registration_units: Optional[list[object]] = None,
    ) -> ProductRegisterResponseWithAssets: ...

