"""Type stubs for FortiCare Products - Details"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, AssetDetail

class ProductDetailsRequest(TypedDict, total=False):
    """ProductDetailsRequest structure."""

    # Serial number
    serialNumber: str

class ProductDetailsResponseAssetdetails(TypedDict, total=False):
    """ProductDetailsResponseAssetdetails structure."""

    # Product model description
    productModel: str
    # Product model EoR date
    productModelEoR: str
    # Product model EoS date
    productModelEoS: str
    # Product serial number
    serialNumber: str
    # Whether the unit has been decommissioned
    isDecommissioned: bool
    # Product registration date in ISO 8601 format
    registrationDate: str
    assetGroups: list
    contracts: list
    # Asset folder id
    folderId: int
    # Asset folder path
    folderPath: str
    # Product description
    description: str
    # Product associated partner name
    partner: str
    # Product associated license information
    license: list[any]
    # Product current support coverage info  
  
    entitlements: list[any]
    location: dict[str, Any]
    warrantySupports: list
    # Warranty type
    warrantyTypeName: str
    # License key information
    licenseKeys: list[any]

class ProductDetailsResponse(TypedDict, total=False):
    """ProductDetailsResponse structure."""

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
    assetDetails: ProductDetailsResponseAssetdetails

class ProductDetailsResponseWithAssetDetails(FortiCareResponse):
    """Specialized response for endpoint with assetDetails."""
    
    @property
    def assetDetails(self) -> AssetDetail:
        """Assetdetails."""
        ...

class ProductDetails:
    """Details operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        serial_number: str,
    ) -> ProductDetailsResponseWithAssetDetails: ...

