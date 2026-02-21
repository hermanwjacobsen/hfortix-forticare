"""Type stubs for FortiCare response models."""

from typing import Any, Iterator, TypeVar, Generic, overload
from .types import AssetInfo, AssetDetailsInfo, LicenseInfo, ContractInfo, FolderInfo

_T = TypeVar('_T')

class FortiCareResponse:
    """Structured wrapper for FortiCare API responses."""
    
    def __init__(
        self,
        data: dict[str, Any],
        http_status_code: int | None = None,
        response_time: float | None = None,
        request_info: dict[str, Any] | None = None,
    ) -> None: ...
    
    # HTTP Metadata Properties
    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        ...
    
    @property
    def response_time(self) -> float | None:
        """Response time in seconds."""
        ...
    
    @property
    def raw(self) -> dict[str, Any]:
        """Raw API response dictionary."""
        ...
    
    @property
    def request_info(self) -> dict[str, Any] | None:
        """HTTP request information (method, url, params, data)."""
        ...
    
    # HTTP Request Metadata (convenience accessors for request_info)
    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        ...
    
    @property
    def http_url(self) -> str | None:
        """Full HTTP request URL."""
        ...
    
    @property
    def http_params(self) -> dict[str, Any] | None:
        """HTTP query parameters."""
        ...
    
    @property
    def http_data(self) -> dict[str, Any] | None:
        """HTTP request body data."""
        ...
    
    @property
    def http_response_time(self) -> float | None:
        """Response time in milliseconds for this API request."""
        ...
    
    @property
    def http_api_request(self) -> dict[str, Any] | None:
        """HTTP API request information for this response."""
        ...
    
    # Common FortiCare Response Fields (for autocomplete)
    @property
    def status(self) -> int | None:
        """API call status code (0 = success, negative = error)."""
        ...
    
    @property
    def message(self) -> str | None:
        """Error message (empty on success)."""
        ...
    
    @property
    def token(self) -> str | None:
        """OAuth access token."""
        ...
    
    @property
    def version(self) -> str | None:
        """API version."""
        ...
    
    @property
    def build(self) -> str | None:
        """API build version."""
        ...
    
    @property
    def error(self) -> str | None:
        """Error details."""
        ...
    
    # Note: __getattr__ is intentionally NOT defined in the stub to force
    # type errors for typos. Use .get() or .raw for dynamic access.
    # At runtime, __getattr__ exists but Pylance won't know about undefined attributes.
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with optional default."""
        ...
    
    def dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        ...
    
    @property
    def json(self) -> str:
        """Get JSON string representation (indented)."""
        ...

class FortiCareObject(Generic[_T]):
    """
    Wrapper for nested objects in FortiCare responses.
    
    Provides attribute access to dictionary/TypedDict fields.
    """
    
    def __init__(self, data: dict[str, Any]) -> None: ...
    
    # For TypedDict objects, provide attribute access
    # Override this in specific subclasses for each type
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with optional default."""
        ...
    
    def dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        ...


class Asset(FortiCareObject[AssetInfo]):
    """Typed wrapper for Asset/Product objects with attribute access."""
    
    @property
    def serialNumber(self) -> str: ...
    
    @property
    def accountId(self) -> int: ...
    
    @property
    def folderId(self) -> int: ...
    
    @property
    def folderPath(self) -> str: ...
    
    @property
    def registrationDate(self) -> str: ...
    
    @property
    def description(self) -> str: ...
    
    @property
    def isDecommissioned(self) -> bool: ...
    
    @property
    def status(self) -> str: ...
    
    @property
    def productModel(self) -> str: ...
    
    @property
    def productModelEoR(self) -> str: ...
    
    @property
    def productModelEoS(self) -> str: ...
    
    @property
    def warrantySupport(self) -> str: ...
    
    @property
    def entitlements(self) -> list: ...


class License(FortiCareObject[LicenseInfo]):
    """Typed wrapper for License objects with attribute access."""
    
    @property
    def serialNumber(self) -> str: ...
    
    @property
    def licenseNumber(self) -> str: ...
    
    @property
    def registrationCode(self) -> str: ...
    
    @property
    def description(self) -> str: ...
    
    @property
    def startDate(self) -> str: ...
    
    @property
    def endDate(self) -> str: ...
    
    @property
    def status(self) -> str: ...


class Contract(FortiCareObject[ContractInfo]):
    """Typed wrapper for Contract objects with attribute access."""
    
    @property
    def contractNumber(self) -> str: ...
    
    @property
    def startDate(self) -> str: ...
    
    @property
    def endDate(self) -> str: ...
    
    @property
    def products(self) -> FortiCareList[Product]: ...
    
    @property
    def status(self) -> str: ...


class Product(FortiCareObject):
    """Typed wrapper for Product objects with attribute access."""
    
    @property
    def serial(self) -> str: ...
    
    @property
    def model(self) -> str: ...


class Folder(FortiCareObject[FolderInfo]):
    """Typed wrapper for Folder objects with attribute access."""
    
    @property
    def folderId(self) -> int: ...
    
    @property
    def folderName(self) -> str: ...
    
    @property
    def folderPath(self) -> str: ...
    
    @property
    def parentFolderId(self) -> int: ...
    
    @property
    def assetCount(self) -> int: ...


class AssetDetail(FortiCareObject[AssetDetailsInfo]):
    """Typed wrapper for AssetDetails object with attribute access."""
    
    @property
    def productModel(self) -> str: ...
    
    @property
    def productModelEoR(self) -> str: ...
    
    @property
    def productModelEoS(self) -> str: ...
    
    @property
    def serialNumber(self) -> str: ...
    
    @property
    def isDecommissioned(self) -> bool: ...
    
    @property
    def registrationDate(self) -> str: ...
    
    @property
    def assetGroups(self) -> list: ...
    
    @property
    def contracts(self) -> list: ...
    
    @property
    def folderId(self) -> int: ...
    
    @property
    def folderPath(self) -> str: ...
    
    @property
    def description(self) -> str: ...
    
    @property
    def partner(self) -> str: ...
    
    @property
    def license(self) -> list: ...
    
    @property
    def entitlements(self) -> list: ...
    
    @property
    def location(self) -> dict: ...
    
    @property
    def warrantySupports(self) -> list: ...
    
    @property
    def warrantyTypeName(self) -> str: ...
    
    @property
    def licenseKeys(self) -> list: ...
    
    @property
    def accountId(self) -> int: ...


class FortiCareList(Generic[_T]):
    """Wrapper for lists in FortiCare responses with generic typing."""
    
    def __init__(self, data: list[Any]) -> None: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __getitem__(self, index: int) -> _T: ...
    def __len__(self) -> int: ...

__all__: list[str]
