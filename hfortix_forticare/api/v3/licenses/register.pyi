"""Type stubs for FortiCare Licenses - Register"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, AssetDetail

class LicenseRegisterRequest(TypedDict, total=False):
    """LicenseRegisterRequest structure."""

    # Optional product serial number, if this field is not empty, the licens
    serialNumber: str
    # License's account ID. Optional for API user with Local scope, mandator
    accountId: int
    # License registration code
    licenseRegistrationCode: str
    # Optional, the description for the new product
    description: str
    # Store extra info for certain product registration, for example system 
    additionalInfo: str
    # Product will be used for government or not
    isGovernment: bool

class LicenseRegisterResponseAssetdetails(TypedDict, total=False):
    """LicenseRegisterResponseAssetdetails structure."""

    # Product model description
    productModel: str
    # Product serial number
    serialNumber: str
    # Product description
    description: str
    isDecommissioned: bool
    # Product associated partner name
    partner: str
    # Registration date
    registrationDate: str
    warrantySupports: list
    assetGroups: list
    contracts: list
    productModelEoR: str
    productModelEoS: str
    # product associated license information
    license: list[any]
    # product current support coverage info  
    entitlements: list[any]
    location: dict[str, Any]

class LicenseRegisterResponse(TypedDict, total=False):
    """LicenseRegisterResponse structure."""

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
    assetDetails: LicenseRegisterResponseAssetdetails

class LicenseRegisterResponseWithAssetDetails(FortiCareResponse):
    """Specialized response for endpoint with assetDetails."""
    
    @property
    def assetDetails(self) -> AssetDetail:
        """Assetdetails."""
        ...

class LicenseRegister:
    """Register operations for licenses endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        license_registration_code: str,
        account_id: Optional[int] = None,
        additional_info: Optional[str] = None,
        description: Optional[str] = None,
        is_government: Optional[bool] = None,
        serial_number: Optional[str] = None,
    ) -> LicenseRegisterResponseWithAssetDetails: ...

