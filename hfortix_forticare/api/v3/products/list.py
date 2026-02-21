"""
FortiCare Products - List

Returns products that have entitlements

API Endpoint:
    post /products/list

<ul><li>Retrieves a list of products based on provided filter parameters.</li><li>At least one of serialNumber or expireBefore must be specified.</li><li>The endpoint returns only products that have entitlement, and whose entitlement matches the expireBefore criteria (if provided).</li><li>Products may or may not have contracts associated with them.</li></ul>
Required permission: Read

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call list endpoint
    >>> response = fcc.api.products.list.post(serial_number=..., expire_before=...)
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

__all__ = ["ProductList"]


class ProductListRequest(TypedDict, total=False):
    """ProductListRequest structure."""

    # Serial number or serial number search pattern
    serialNumber: str
    # Date time in ISO 8601 format. Return products with entitlement expirin
    expireBefore: str
    # Allowed values are Registered and Pending. Default value is Registered
    status: str
    # Product model name (optional)
    productModel: str
    # Optional parameter for API user with Local scope, mandatory for Org sc
    accountId: int

class ProductListResponse(TypedDict, total=False):
    """ProductListResponse structure."""

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

class ProductListResponseWithAssets(FortiCareResponse):
    """Specialized response for endpoint with assets."""
    
    @property
    def assets(self):
        """Assets."""
        return super().__getattribute__("__getattr__")("assets")


class ProductList:
    """List operations for products endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize List endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/products/list"
    
    def post(
        self,
        account_id: Optional[int] = None,
        expire_before: Optional[str] = None,
        product_model: Optional[str] = None,
        serial_number: Optional[str] = "%",
        status: Optional[str] = None,
    ) -> ProductListResponseWithAssets:
        """
        Returns products that have entitlements
        
        <ul><li>Retrieves a list of products based on provided filter parameters.</li><li>At least one of serialNumber or expireBefore must be specified.</li><li>The endpoint returns only products that have entitlement, and whose entitlement matches the expireBefore criteria (if provided).</li><li>Products may or may not have contracts associated with them.</li></ul>
Required permission: Read
        
        Args:
            serial_number: Use SQL LIKE wildcards (%). Defaults to '%' (all products). Set to None to use expireBefore instead. (optional)
            expire_before: Date time in ISO 8601 format. Return products with entitlement expiring before this date. (optional)
            status: Allowed values are Registered and Pending. Default value is Registered. (optional)
            product_model: Product model name (optional) (optional)
            account_id: Optional parameter for API user with Local scope, mandatory for Org scope (optional)
        
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
            >>> response = endpoint.post(serial_number=..., expire_before=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
        }

        if serial_number is not None:
            request_data['serialNumber'] = serial_number
        if expire_before is not None:
            request_data['expireBefore'] = expire_before
        if status is not None:
            request_data['status'] = status
        if product_model is not None:
            request_data['productModel'] = product_model
        if account_id is not None:
            request_data['accountId'] = account_id
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return ProductListResponseWithAssets(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
