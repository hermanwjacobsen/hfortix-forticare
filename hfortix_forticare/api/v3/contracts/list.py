"""
FortiCare Contracts - List

Returns list of contracts based on given criteria

API Endpoint:
    post /contracts/list

Return list of contracts
Required permission: ReadOnly

Example Usage:
    >>> from hfortix_forticare import FortiCare
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>>
    >>> # Call list endpoint
    >>> response = fcc.api.contracts.list.post(contract_number=..., account_id=...)
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

__all__ = ["ContractList"]


class ContractListRequest(TypedDict, total=False):
    """ContractListRequest structure."""

    # Optional contract number
    contractNumber: str
    # Contract's account ID. Optional for API user with Local scope, mandato
    accountId: int
    # Optional SKU
    contractSKU: str
    # Optional status. Allowed values are Registered and Pending.
    status: str

class ContractListResponse(TypedDict, total=False):
    """ContractListResponse structure."""

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
    contracts: list[any]

class ContractListResponseWithContracts(FortiCareResponse):
    """Specialized response for endpoint with contracts."""
    
    @property
    def contracts(self):
        """Contracts."""
        return super().__getattribute__("__getattr__")("contracts")


class ContractList:
    """List operations for contracts endpoints."""
    
    def __init__(self, client: CloudHTTPClient):
        """
        Initialize List endpoint.
        
        Args:
            client: HTTP client instance for API communication
        """
        self._client = client
        self._path = "/contracts/list"
    
    def post(
        self,
        account_id: Optional[int] = None,
        contract_number: Optional[str] = None,
        contract_sku: Optional[str] = None,
        status: Optional[str] = None,
    ) -> ContractListResponseWithContracts:
        """
        Returns list of contracts based on given criteria
        
        Return list of contracts
Required permission: ReadOnly
        
        Args:
            contract_number: Optional contract number (optional)
            account_id: Contract's account ID. Optional for API user with Local scope, mandatory for Org scope. (optional)
            contract_sku: Optional SKU (optional)
            status: Optional status. Allowed values are Registered and Pending. (optional)
        
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
            >>> response = endpoint.post(contract_number=..., account_id=...)
            >>> if response.status == 0:
            ...     print("Success!")
            ...     print(f"Took {response.response_time:.2f}s")
        """
        # Build request body
        request_data = {
        }

        if contract_number is not None:
            request_data['contractNumber'] = contract_number
        if account_id is not None:
            request_data['accountId'] = account_id
        if contract_sku is not None:
            request_data['contractSKU'] = contract_sku
        if status is not None:
            request_data['status'] = status
        
        # Make API call (returns envelope with data, http_status_code, response_time, request_info)
        envelope = self._client.post(
            self._path,
            data=request_data,
        )
        
        # Wrap in FortiCareResponse for attribute access
        return ContractListResponseWithContracts(
            data=envelope["data"],
            http_status_code=envelope["http_status_code"],
            response_time=envelope["response_time"],
            request_info=envelope["request_info"],
        )
