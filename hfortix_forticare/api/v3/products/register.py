"""
FortiCare Products - Register

Register multiple products and contracts in one request

API Endpoint:
    post /products/register

Register multiple products/contracts in one request
Required permission: ReadWrite/Admin<ul><li>"countryCode" follows ISO 3166 Alpha-2 codes</li><li>For certain countries (United States, Canada, India, Brazil and Ukraine), "stateOrProvince" must be one of standard 2-letter abbreviations for the corresponding country</li><li>"phone" and "fax" must follow this format (without brackets): "+(country code)(space)(number)"</li></ul>

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call register endpoint
    >>> response = fcc.api.products.register.post(account_id=..., registration_units=...)
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

__all__ = ["ProductRegister"]


class ProductRegisterRequest(TypedDict, total=False):
    """ProductRegisterRequest structure."""

    # Product's Account ID. Optional for API user with Local scope, mandator
    accountId: int
    registrationUnits: list[object]
    locations: list[object]

class ProductRegisterResponse(TypedDict, total=False):
    """ProductRegisterResponse structure."""

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
    assets: list[any]

class ProductRegisterResponseWithAssets(FortiCareResponse):
    """Specialized response for endpoint with assets."""
    
    @property
    def assets(self):
        """Assets."""
        items = super().__getattribute__("__getattr__")("assets")
        return items[0] if items else None


class ProductRegister:
    """Register operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize Register endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/register"
    
    def post(
        self,
        account_id: Optional[int] = None,
        locations: Optional[list[object]] = None,
        registration_units: Optional[list[object]] = None,
    ) -> ProductRegisterResponseWithAssets:
        """
        Register multiple products and contracts in one request
        
        Register multiple products/contracts in one request
Required permission: ReadWrite/Admin<ul><li>"countryCode" follows ISO 3166 Alpha-2 codes</li><li>For certain countries (United States, Canada, India, Brazil and Ukraine), "stateOrProvince" must be one of standard 2-letter abbreviations for the corresponding country</li><li>"phone" and "fax" must follow this format (without brackets): "+(country code)(space)(number)"</li></ul>
        
        Args:
            account_id: Product's Account ID. Optional for API user with Local scope, mandatory for Org scope. (optional)
            registration_units:  (optional)
            locations:  (optional)
        
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
            >>> response = endpoint.post(account_id=..., registration_units=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
        }

        if account_id is not None:
            request_data['accountId'] = account_id
        if registration_units is not None:
            request_data['registrationUnits'] = registration_units
        if locations is not None:
            request_data['locations'] = locations
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return ProductRegisterResponseWithAssets(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
