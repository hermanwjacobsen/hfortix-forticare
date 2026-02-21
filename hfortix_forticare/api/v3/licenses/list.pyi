"""Type stubs for FortiCare Licenses - List"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, License

class LicenseListRequest(TypedDict, total=False):
    """LicenseListRequest structure."""

    # Optional license number
    licenseNumber: str
    # License's account ID. Optional for API user with Local scope, mandator
    accountId: int
    # Optional SKU
    licenseSKU: str
    # Optional status. Allowed values are Registered and Pending.
    status: str

class LicenseListResponse(TypedDict, total=False):
    """LicenseListResponse structure."""

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
    licenses: list[any]

class LicenseListResponseWithLicenses(FortiCareResponse):
    """Specialized response for endpoint with licenses."""
    
    @property
    def licenses(self) -> FortiCareList[License]:
        """Licenses."""
        ...

class LicenseList:
    """List operations for licenses endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        account_id: Optional[int] = None,
        license_number: Optional[str] = None,
        license_sku: Optional[str] = None,
        status: Optional[str] = None,
    ) -> LicenseListResponseWithLicenses: ...

