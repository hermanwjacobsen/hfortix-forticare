"""
FortiCare Asset Management API Client - Type Stubs

Python SDK for Fortinet FortiCare Asset Management V3 API.
"""

from __future__ import annotations

from typing import Any, Optional
from hfortix_core.session import CloudSession
from .api.v3 import V3API
from .models import FortiCareResponse, FortiCareObject, FortiCareList, Product

__version__: str

class FortiCare:
    """
    FortiCare Asset Management API Client.
    
    Main entry point for interacting with FortiCare Asset Management V3 API.
    """
    
    DEFAULT_CLIENT_ID: str
    api: V3API
    
    def __init__(
        self,
        api_id: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        oauth_token: Optional[str] = None,
        session: Optional[CloudSession] = None,
        base_url: str = "https://support.fortinet.com/ES/api/registration/v3",
        auth_url: Optional[str] = None,
        verify: bool = True,
        max_retries: int = 3,
        connect_timeout: float = 10.0,
        read_timeout: float = 300.0,
        read_only: bool = False,
        track_operations: bool = False,
        audit_handler: Optional[Any] = None,
        audit_callback: Optional[Any] = None,
        user_context: Optional[dict[str, Any]] = None,
        rate_limit_calls_per_min: Optional[int] = None,
        rate_limit_calls_per_5min: Optional[int] = None,
        rate_limit_calls_per_hour: Optional[int] = None,
        rate_limit_errors_per_min: Optional[int] = None,
        rate_limit_errors_per_5min: Optional[int] = None,
        rate_limit_errors_per_hour: Optional[int] = None,
    ) -> None: ...
    
    def get_rate_limit_status(self) -> dict[str, Any]: ...
    def get_retry_stats(self) -> dict[str, Any]: ...
    def get_circuit_breaker_state(self) -> dict[str, Any]: ...
    def get_health_metrics(self) -> dict[str, Any]: ...
    def get_operations(self) -> list[dict[str, Any]]: ...
    def get_write_operations(self) -> list[dict[str, Any]]: ...
    def get_connection_stats(self) -> dict[str, Any]: ...
    def inspect_last_request(self) -> Optional[dict[str, Any]]: ...
    def login(self, force_refresh: bool = False) -> dict[str, Any]: ...
    def refresh_token(self) -> dict[str, Any]: ...
    def get_token_time_remaining(self) -> Optional[int]: ...
    def is_token_expired(self, buffer_seconds: int = 0) -> bool: ...
    def get_token_info(self) -> dict[str, Any]: ...
    def logout(self) -> None: ...
    
    def __enter__(self) -> FortiCare: ...
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
    
    def __repr__(self) -> str: ...

__all__ = [
    "FortiCare",
    "FortiCareResponse",
    "FortiCareObject",
    "FortiCareList",
    "Product",
]

