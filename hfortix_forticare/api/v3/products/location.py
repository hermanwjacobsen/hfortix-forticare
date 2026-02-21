"""
FortiCare Products - Location

Update location of a product

API Endpoint:
    post /products/location

Update or delete (pass null as parameter) location of a product using serial number
Required permission: ReadWrite/Admin<ul><li>"countryCode" follows ISO 3166 Alpha-2 codes</li><li>For certain countries (United States, Canada, India, Brazil and Ukraine), "stateOrProvince" must be one of standard 2-letter abbreviations for the corresponding country</li><li>"phone" and "fax" must follow this format (without brackets): "+(country code)(space)(number)"</li></ul>

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call location endpoint
    >>> response = fcc.api.products.location.post(serial_number=..., location=...)
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

__all__ = ["ProductLocation"]


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
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Location endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/location"
    
    def post(
        self,
        serial_number: str,
        location: Optional[dict[str, Any]] = None,
    ) -> FortiCareResponse:
        """
        Update location of a product
        
        Update or delete (pass null as parameter) location of a product using serial number
Required permission: ReadWrite/Admin<ul><li>"countryCode" follows ISO 3166 Alpha-2 codes</li><li>For certain countries (United States, Canada, India, Brazil and Ukraine), "stateOrProvince" must be one of standard 2-letter abbreviations for the corresponding country</li><li>"phone" and "fax" must follow this format (without brackets): "+(country code)(space)(number)"</li></ul>
        
        Args:
            serial_number: Product serial number (required)
            location:  (optional)
        
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
            >>> response = endpoint.post(serial_number=..., location=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
            'serialNumber': serial_number,
        }

        if location is not None:
            request_data['location'] = location
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return FortiCareResponse(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
