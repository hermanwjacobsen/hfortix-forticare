"""Type stubs for FortiCare Contracts - List"""

from typing import Any, Optional, TypedDict
from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_forticare.models import FortiCareResponse, FortiCareList, Contract

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
    def contracts(self) -> FortiCareList[Contract]:
        """Contracts."""
        ...

class ContractList:
    """List operations for contracts endpoints."""
    
    def __init__(self, client: CloudHTTPClient) -> None: ...
    
    def post(
        self,
        account_id: Optional[int] = None,
        contract_number: Optional[str] = None,
        contract_sku: Optional[str] = None,
        status: Optional[str] = None,
    ) -> ContractListResponseWithContracts: ...

