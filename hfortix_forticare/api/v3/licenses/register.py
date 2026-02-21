"""
FortiCare Licenses - Register

Register license

API Endpoint:
    post /licenses/register

Used for registering license
Required permission: ReadWrite/Admin

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call register endpoint
    >>> response = fcc.api.licenses.register.post(serial_number=..., account_id=...)
    >>>
    >>> # Access response data as attributes
    >>> print(response.status)  # 0 for success
    >>> print(response.message)  # Error message (if any)
    >>>
    >>> # Access HTTP metadata
    >>> print(response.http_status_code)  # 200, 404, etc.
    >>> print(response.response_time)  # Request duration
    >>>
    >>> # Get raw response
    >>> raw_dict = response.raw
    >>> dict_copy = response.dict()

Important:
    - Requires OAuth 2.0 Bearer token authentication
    - Rate limits: 100 calls/min, 1000 calls/hour

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, TypedDict

if TYPE_CHECKING:
    from hfortix_core.http.cloud_client import CloudHTTPClient

from hfortix_forticare.models import FortiCareResponse

__all__ = ["LicenseRegister"]


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
    def assetDetails(self):
        """Assetdetails."""
        return super().__getattribute__("__getattr__")("assetDetails")


class LicenseRegister:
    """Register operations for licenses endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Register endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/licenses/register"
    
    def post(
        self,
        license_registration_code: str,
        account_id: Optional[int] = None,
        additional_info: Optional[str] = None,
        description: Optional[str] = None,
        is_government: Optional[bool] = None,
        serial_number: Optional[str] = None,
    ) -> LicenseRegisterResponseWithAssetDetails:
        """
        Register license
        
        Used for registering license
Required permission: ReadWrite/Admin
        
        Args:
            serial_number: Optional product serial number, if this field is not empty, the license will be registered under it, otherwise a virtual product will be created for the registered license (if applicable) (optional)
            account_id: License's account ID. Optional for API user with Local scope, mandatory for Org scope. (optional)
            license_registration_code: License registration code (required)
            description: Optional, the description for the new product (optional)
            additional_info: Store extra info for certain product registration, for example system ID, IP address etc. (optional)
            is_government: Product will be used for government or not (optional)
        
        Returns:
            FortiCareResponse object with:
            - Attribute access to all response fields
            - .http_status_code: HTTP status code (200, 404, etc.)
            - .response_time: Request duration in seconds
            - .raw: Full response dictionary
            - .dict(): Convert to plain dict
            
            Response fields:
            - token: OAuth access token
            - version: API version
            - status: API call status code, 0 means success
            - message: Error message in case the request fails, empty message means success
            - error: 
        
        Raises:
            httpx.HTTPStatusError: For HTTP error responses
            httpx.TimeoutException: If request times out
            httpx.RequestError: For network errors
        
        Example:
            >>> response = endpoint.post(serial_number=..., account_id=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
            'licenseRegistrationCode': license_registration_code,
        }

        if serial_number is not None:
            request_data['serialNumber'] = serial_number
        if account_id is not None:
            request_data['accountId'] = account_id
        if description is not None:
            request_data['description'] = description
        if additional_info is not None:
            request_data['additionalInfo'] = additional_info
        if is_government is not None:
            request_data['isGovernment'] = is_government
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return LicenseRegisterResponseWithAssetDetails(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
