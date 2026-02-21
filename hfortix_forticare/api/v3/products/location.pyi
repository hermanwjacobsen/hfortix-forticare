"""Type stubs for FortiCare Products - Location"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse

class ProductLocationRequestLocation(TypedDict, total=False):
    """ProductLocationRequestLocation structure."""

    # Company name
    company: str
    # Address of the location
    address: str
    # City name
    city: str
    # State or province name
    stateOrProvince: str
    # Two letter country code
    countryCode: str
    # Zip/postal code of the location
    postalCode: str
    # Email address
    email: str
    # Phone number
    phone: str
    # Fax number
    fax: str

class ProductLocationRequest(TypedDict, total=False):
    """ProductLocationRequest structure."""

    # Product serial number
    serialNumber: str
    location: ProductLocationRequestLocation

class ProductLocationResponse(TypedDict, total=False):
    """ProductLocationResponse structure."""

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

class ProductLocation:
    """Location operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        serial_number: str,
        location: Optional[dict[str, Any]] = None,
    ) -> FortiCareResponse: ...

