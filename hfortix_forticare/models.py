"""
FortiCare Response Models

Provides structured response objects for FortiCare Asset Management API.
"""

from __future__ import annotations

from typing import Any, Iterator


class FortiCareResponse:
    """
    Structured wrapper for FortiCare API responses.
    
    Provides clean attribute access to API response data with metadata.
    
    Features:
    - Attribute access to response fields: response.status, response.message
    - HTTP metadata: response.http_status_code, response.response_time
    - Raw data access: response.raw, response.dict()
    - Iteration support for list responses
    
    Examples:
        >>> response = fcc.api.products.list.post(serial_number="FGT*")
        >>>
        >>> # Attribute access
        >>> response.status  # 0 for success
        >>> response.message  # Error message or empty
        >>> response.token  # OAuth token
        >>>
        >>> # Iterate over results (if list response)
        >>> for product in response.assets:
        ...     print(product.serialNumber)
        >>>
        >>> # HTTP metadata
        >>> response.http_status_code  # 200, 404, etc.
        >>> response.response_time  # Request duration in seconds
        >>>
        >>> # Raw access
        >>> response.raw  # Full API response dict
        >>> response.dict()  # Convert to dict
    
    Args:
        data: Dictionary from FortiCare API response
        http_status_code: HTTP status code (200, 404, 500, etc.)
        response_time: Response time in seconds
        request_info: HTTP request information
    """
    
    def __init__(
        self,
        data: dict[str, Any],
        http_status_code: int | None = None,
        response_time: float | None = None,
        request_info: dict[str, Any] | None = None,
    ):
        """
        Initialize FortiCare response object.
        
        Args:
            data: Dictionary containing the API response fields
            http_status_code: HTTP status code from response
            response_time: Response time in seconds
            request_info: Request metadata (method, url, params, data)
        """
        self._data = data
        self._http_status_code = http_status_code
        self._response_time = response_time
        self._request_info = request_info
    
    # ========================================================================
    # Metadata Properties
    # ========================================================================
    
    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        return self._http_status_code
    
    @property
    def response_time(self) -> float | None:
        """Response time in seconds."""
        return self._response_time
    
    @property
    def raw(self) -> dict[str, Any]:
        """Raw API response dictionary."""
        return self._data
    
    @property
    def request_info(self) -> dict[str, Any] | None:
        """HTTP request information (method, url, params, data)."""
        return self._request_info
    
    # ========================================================================
    # HTTP Request Metadata (convenience accessors for request_info)
    # ========================================================================
    
    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        return self._request_info.get("method") if self._request_info else None
    
    @property
    def http_url(self) -> str | None:
        """Full HTTP request URL."""
        return self._request_info.get("url") if self._request_info else None
    
    @property
    def http_params(self) -> dict[str, Any] | None:
        """HTTP query parameters."""
        return self._request_info.get("params") if self._request_info else None
    
    @property
    def http_data(self) -> dict[str, Any] | None:
        """HTTP request body data."""
        return self._request_info.get("data") if self._request_info else None
    
    @property
    def http_response_time(self) -> float | None:
        """
        Response time in milliseconds for this API request.
        
        Returns None if timing was not tracked.
        
        Examples:
            >>> result = fcc.api.products.list.post()
            >>> print(f"Query took {result.http_response_time:.1f}ms")
            Query took 45.2ms
        """
        return self._response_time * 1000 if self._response_time else None
    
    @property
    def http_api_request(self) -> dict[str, Any] | None:
        """
        HTTP API request information for this response.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full URL that was requested
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> result = fcc.api.products.list.post(serial_number="FGT*")
            >>> print(result.http_api_request)
            {
                'method': 'POST',
                'url': 'https://support.fortinet.com/ES/api/v3/products/list',
                'params': {},
                'data': {'serial_number': 'FGT*'}
            }
        """
        return self._request_info
    
    # ========================================================================
    # Common FortiCare Response Fields (for autocomplete)
    # ========================================================================
    
    @property
    def status(self) -> int | None:
        """API call status code (0 = success, negative = error)."""
        return self._data.get("status")
    
    @property
    def message(self) -> str | None:
        """Error message (empty on success)."""
        return self._data.get("message")
    
    @property
    def token(self) -> str | None:
        """OAuth access token."""
        return self._data.get("token")
    
    @property
    def version(self) -> str | None:
        """API version."""
        return self._data.get("version")
    
    @property
    def build(self) -> str | None:
        """API build version."""
        return self._data.get("build")
    
    @property
    def error(self) -> str | None:
        """Error details."""
        return self._data.get("error")
    
    # ========================================================================
    # Dynamic Attribute Access
    # ========================================================================
    
    def __getattr__(self, name: str) -> Any:
        """
        Dynamic attribute access for response fields.
        
        Allows accessing any field from the API response as an attribute.
        For nested objects/lists, wraps them in FortiCareObject for consistency.
        
        Args:
            name: Attribute name
            
        Returns:
            Field value from response data, or None if field doesn't exist
            
        Raises:
            AttributeError: Only for private attributes (starting with _)
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        # Generic convenience property: singular form returns first item from plural arrays
        # e.g., assetFolder -> assetFolders[0], asset -> assets[0], license -> licenses[0]
        plural_name = name + 's'
        if plural_name in self._data:
            items = self._data[plural_name]
            if isinstance(items, list) and len(items) > 0:
                return FortiCareObject(items[0])
            return None  # Return None if array is empty
        
        if name in self._data:
            value = self._data[name]
            
            # Wrap lists in FortiCareList for iteration
            if isinstance(value, list):
                return FortiCareList(value)
            
            # Wrap dicts in FortiCareObject for attribute access
            if isinstance(value, dict):
                return FortiCareObject(value)
            
            return value
        
        # Return None for missing fields instead of raising AttributeError
        # This allows accessing optional fields without try/except blocks
        return None
    
    def __dir__(self) -> list[str]:
        """List available attributes (for autocomplete)."""
        # Include both object properties and data fields
        return list(set(
            list(object.__dir__(self)) +
            [k for k in self._data.keys() if isinstance(k, str)]
        ))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with optional default."""
        return self._data.get(key, default)
    
    def dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self._data.copy()
    
    @property
    def json(self) -> str:
        """
        Get JSON string representation (indented).
        
        Returns:
            Pretty-printed JSON string with 2-space indentation
            
        Example:
            >>> response = fcc.api.products.list.post()
            >>> print(response.json)  # No parentheses - it's a property
        """
        import json
        return json.dumps(self._data, indent=2)
    
    def __repr__(self) -> str:
        """String representation."""
        status = self._data.get("status", "unknown")
        return f"FortiCareResponse(status={status}, fields={len(self._data)})"
    
    def __str__(self) -> str:
        """String representation."""
        import json
        return json.dumps(self._data, indent=2)


class FortiCareObject:
    """
    Wrapper for nested objects in FortiCare responses.
    
    Provides attribute access to dictionary fields.
    
    Example:
        >>> asset = response.assets[0]  # FortiCareObject
        >>> asset.serialNumber
        >>> asset.productModel
        >>> asset.description
    """
    
    def __init__(self, data: dict[str, Any]):
        """Initialize with dictionary data."""
        self._data = data
    
    def __getattr__(self, name: str) -> Any:
        """
        Dynamic attribute access.
        
        Returns:
            Field value, or None if field doesn't exist
            
        Raises:
            AttributeError: Only for private attributes (starting with _)
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        if name in self._data:
            value = self._data[name]
            
            # Recursively wrap nested structures
            if isinstance(value, dict):
                return FortiCareObject(value)
            if isinstance(value, list):
                return FortiCareList(value)
            
            return value
        
        # Return None for missing fields instead of raising AttributeError
        # This allows accessing optional fields without try/except blocks
        return None
    
    def __dir__(self) -> list[str]:
        """List available attributes."""
        return list(set(
            list(object.__dir__(self)) +
            [k for k in self._data.keys() if isinstance(k, str)]
        ))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with optional default."""
        return self._data.get(key, default)
    
    def dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self._data.copy()
    
    def __repr__(self) -> str:
        """String representation."""
        return f"FortiCareObject({self._data})"


class FortiCareList:
    """
    Wrapper for lists in FortiCare responses.
    
    Provides iteration and indexing with automatic object wrapping.
    
    Example:
        >>> for asset in response.assets:  # FortiCareList iteration
        ...     print(asset.serialNumber)  # Each item is FortiCareObject
    """
    
    def __init__(self, data: list[Any]):
        """Initialize with list data."""
        self._data = data
    
    def __iter__(self) -> Iterator[Any]:
        """Iterate over items, wrapping dicts in FortiCareObject."""
        for item in self._data:
            if isinstance(item, dict):
                yield FortiCareObject(item)
            else:
                yield item
    
    def __getitem__(self, index: int) -> Any:
        """Get item by index, wrapping dicts in FortiCareObject."""
        item = self._data[index]
        if isinstance(item, dict):
            return FortiCareObject(item)
        return item
    
    def __len__(self) -> int:
        """Get list length."""
        return len(self._data)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"FortiCareList({len(self._data)} items)"


__all__ = [
    "FortiCareResponse",
    "FortiCareObject",
    "FortiCareList",
    "Asset",
    "License",
    "Contract",
    "Product",
    "Folder",
]


# Typed wrapper classes for specific response object types
# These are just aliases - they use the base FortiCareObject implementation
# but the .pyi stubs provide specific property types for each

class Asset(FortiCareObject):
    """Typed wrapper for Asset/Product objects."""
    pass


class License(FortiCareObject):
    """Typed wrapper for License objects."""
    pass


class Contract(FortiCareObject):
    """Typed wrapper for Contract objects."""
    pass


class Product(FortiCareObject):
    """Typed wrapper for Product objects (nested in contracts, etc)."""
    pass


class Folder(FortiCareObject):
    """Typed wrapper for Folder objects."""
    pass

