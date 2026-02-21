"""Type stubs for FortiCare Products - Decommission"""

from typing import Any, Optional, TypedDict, Union
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse

class ProductDecommissionRequest(TypedDict, total=False):
    """ProductDecommissionRequest structure."""

    # Product serial number(s)
    serialNumbers: list

class ProductDecommissionResponse(TypedDict, total=False):
    """ProductDecommissionResponse structure."""

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

class ProductDecommission:
    """Decommission operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        serial_numbers: Union[str, list[str]],
    ) -> FortiCareResponse: ...

