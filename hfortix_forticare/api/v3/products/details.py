"""
FortiCare Products - Details

Returns product detailed information, including active support coverage and associated licenses

API Endpoint:
    post /products/details

Used to get product details
Required permission: Read 

 Quantity of support seats can be found under relevant support type in Entitlements section of Response: 
 <ul><li>Number of CPUs for subscription-based models: support type 113</li><li> VDOMs: support type 207 </li><li> ADOMs: support type 152</li></ul>

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call details endpoint
    >>> response = fcc.api.products.details.post(serial_number=...)
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

__all__ = ["ProductDetails"]


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
    def assetDetails(self):
        """Assetdetails."""
        return super().__getattribute__("__getattr__")("assetDetails")


class ProductDetails:
    """Details operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Details endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/details"
    
    def post(
        self,
        serial_number: str,
    ) -> ProductDetailsResponseWithAssetDetails:
        """
        Returns product detailed information, including active support coverage and associated licenses
        
        Used to get product details
Required permission: Read 

 Quantity of support seats can be found under relevant support type in Entitlements section of Response: 
 <ul><li>Number of CPUs for subscription-based models: support type 113</li><li> VDOMs: support type 207 </li><li> ADOMs: support type 152</li></ul>
        
        Args:
            serial_number: Serial number (required)
        
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
            >>> response = endpoint.post(serial_number=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
            'serialNumber': serial_number,
        }

        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return ProductDetailsResponseWithAssetDetails(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
