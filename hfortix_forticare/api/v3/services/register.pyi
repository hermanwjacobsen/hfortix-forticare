"""Type stubs for FortiCare Services - Register"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, AssetDetail

class ServiceRegisterRequest(TypedDict, total=False):
    """ServiceRegisterRequest structure."""

    # Contract number to register
    contractNumber: str
    # Service's account ID. Optional for API user with Local scope, mandator
    accountId: int
    # Set product description during registration process
    description: str
    # Store extra info for certain product registration, for example system 
    additionalInfo: str
    # Whether the product will be used for government or not
    isGovernment: bool

class ServiceRegisterResponse(TypedDict, total=False):
    """ServiceRegisterResponse structure."""

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
    assetDetails: Any

class ServiceRegisterResponseWithAssetDetails(FortiCareResponse):
    """Specialized response for endpoint with assetDetails."""
    
    @property
    def assetDetails(self) -> AssetDetail:
        """Assetdetails."""
        ...

class ServiceRegister:
    """Register operations for services endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        contract_number: str,
        account_id: Optional[int] = None,
        additional_info: Optional[str] = None,
        description: Optional[str] = None,
        is_government: Optional[bool] = None,
    ) -> ServiceRegisterResponseWithAssetDetails: ...

