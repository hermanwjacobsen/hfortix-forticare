"""Type stubs for FortiCare Products - Description"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse

class ProductDescriptionRequest(TypedDict, total=False):
    """ProductDescriptionRequest structure."""

    # Product serial number
    serialNumber: str
    # Description for product
    description: str

class ProductDescriptionResponse(TypedDict, total=False):
    """ProductDescriptionResponse structure."""

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

class ProductDescription:
    """Description operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        serial_number: str,
        description: Optional[str] = None,
    ) -> FortiCareResponse: ...

