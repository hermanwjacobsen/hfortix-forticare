"""Type stubs for FortiCare Licenses - Download"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse

class LicenseDownloadRequest(TypedDict, total=False):
    """LicenseDownloadRequest structure."""

    # Product serial number
    serialNumber: str

class LicenseDownloadResponse(TypedDict, total=False):
    """LicenseDownloadResponse structure."""

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
    # Product serial number
    serialNumber: str
    # License file content
    licenseFile: str

class LicenseDownload:
    """Download operations for licenses endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        serial_number: str,
    ) -> FortiCareResponse: ...

