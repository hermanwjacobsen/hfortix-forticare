"""
FortiCare Asset Management API Client

Python SDK for Fortinet FortiCare Asset Management V3 API.
Provides programmatic access to product registration, licensing,
folder management, and contract information.

Example:
    >>> from hfortix_forticare import FortiCare
    >>> 
    >>> # Initialize with OAuth token
    >>> fcc = FortiCare(oauth_token="your_oauth_token")
    >>> 
    >>> # List products - returns FortiCareResponse object
    >>> response = fcc.api.products.list.post(serial_number="FGT*")
    >>> 
    >>> # Access response as attributes
    >>> print(response.status)  # 0 for success
    >>> print(response.http_status_code)  # 200
    >>> 
    >>> # Iterate over assets (if list response)
    >>> for asset in response.assets:
    ...     print(asset.serialNumber)
    >>> 
    >>> # Register a product
    >>> result = fcc.api.products.register.post(...)
    >>> 
    >>> # Clean up
    >>> fcc.logout()

For more examples, see EXAMPLES.md
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from hfortix_core.http.cloud_client import CloudHTTPClient
from hfortix_core.http.oauth import FortiCloudAuth, get_oauth_token
from hfortix_core.session import CloudSession
from hfortix_core.ratelimit import RateLimitStats
from .api.v3 import V3API
from .models import FortiCareResponse, FortiCareObject, FortiCareList, Product

logger = logging.getLogger("hfortix.forticare")

__version__ = "0.5.161"
__all__ = [
    "FortiCare",
    "FortiCareResponse",
    "FortiCareObject",
    "FortiCareList",
    "Product",
    "FortiCloudAuth",
    "get_oauth_token",
]


class FortiCare:
    """
    FortiCare Asset Management API Client.
    
    Main entry point for interacting with FortiCare Asset Management V3 API.
    Provides OAuth-authenticated access to product registration, licensing,
    folder management, and contract endpoints.
    
    Authentication:
        Automatically obtains OAuth token using API credentials, or accepts
        pre-obtained token, or uses shared CloudSession.
    
    Rate Limits:
        - 100 calls per minute
        - 1000 calls per hour  
        - 10 errors per hour
        - Batch operations: max 10 units, max 5 errors per batch
    
    Attributes:
        api: V3 API endpoints (products, licenses, folders, services, contracts)
    
    Example:
        >>> # Initialize with credentials (auto-login)
        >>> fcc = FortiCare(
        ...     api_id="your_api_id",
        ...     password="your_password",
        ...     client_id="assetmanagement"
        ... )
        >>> products = fcc.api.products.list.post(serial_number="FGT*")
        >>> fcc.logout()
        >>> 
        >>> # Or with pre-obtained token
        >>> fcc = FortiCare(oauth_token="your_token")
        >>> 
        >>> # Or with CloudSession (recommended for multi-service)
        >>> with CloudSession(api_id="...", password="...") as session:
        ...     fcc = FortiCare(session=session)  # Auto uses "assetmanagement"
        ...     products = fcc.api.products.list.post()
    """
    
    # Default OAuth client_id for FortiCare Asset Management
    DEFAULT_CLIENT_ID = "assetmanagement"
    
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
        # OLD Rate limiting configuration (set to None by default - configure as needed)
        rate_limit_calls_per_min: Optional[int] = None,
        rate_limit_calls_per_5min: Optional[int] = None,
        rate_limit_calls_per_hour: Optional[int] = None,
        rate_limit_errors_per_min: Optional[int] = None,
        rate_limit_errors_per_5min: Optional[int] = None,
        rate_limit_errors_per_hour: Optional[int] = None,
        # NEW: Rate limiting enforcement parameters
        rate_limit: bool = False,
        rate_limit_strategy: str = "queue",
        rate_limit_max_requests: int = 100,
        rate_limit_window_seconds: float = 60.0,
        rate_limit_queue_size: int = 100,
        rate_limit_queue_timeout: float = 30.0,
        rate_limit_queue_overflow: str = "block",
        circuit_breaker: bool = False,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: float = 60.0,
        circuit_breaker_half_open_calls: int = 3,
    ):
        """
        Initialize FortiCare client.
        
        Args:
            api_id: FortiCloud API ID (for auto-login)
            password: FortiCloud password (for auto-login)
            client_id: Client ID for service (default: assetmanagement)
            oauth_token: Pre-obtained OAuth token (alternative to api_id/password)
            session: CloudSession for multi-service token management (recommended)
            base_url: FortiCare API base URL (default: https://support.fortinet.com/ES/api/registration/v3)
            auth_url: Authentication URL (default: FortiCloud OAuth endpoint)
            verify: Enable SSL certificate verification (default: True)
            max_retries: Maximum retry attempts for failed requests (default: 3)
            connect_timeout: Connection timeout in seconds (default: 10.0)
            read_timeout: Read timeout in seconds (default: 300.0)
            read_only: Enable read-only mode - simulate write operations without executing (default: False)
            track_operations: Enable operation tracking - maintain audit log of all API calls (default: False)
            audit_handler: Handler for audit logging (implements AuditHandler protocol)
            audit_callback: Custom callback function for audit logging
            user_context: Optional dict with user/application context to include in audit logs
            rate_limit_calls_per_minute: Maximum calls per minute (default: 100, None = no limit)
            rate_limit_calls_per_hour: Maximum calls per hour (default: 1000, None = no limit)
            rate_limit_errors_per_hour: Maximum errors per hour (default: 10, None = no limit)
        
        Raises:
            ValueError: If no authentication method provided
        
        Example:
            >>> # Auto-login with credentials
            >>> fcc = FortiCare(
            ...     api_id="your_api_id",
            ...     password="your_password"
            ... )
            >>> 
            >>> # Or use CloudSession (recommended for multi-service)
            >>> with CloudSession(api_id="...", password="...") as session:
            ...     fcc = FortiCare(session=session)
            ...     fz = FortiZTP(session=session)
            ...     # Both share tokens from same session
            >>> 
            >>> # Or use existing token with audit logging
            >>> from hfortix_core.audit import FileHandler
            >>> fcc = FortiCare(
            ...     oauth_token="abc123...",
            ...     track_operations=True,
            ...     audit_handler=FileHandler("/var/log/forticare-audit.jsonl"),
            ...     user_context={"username": "admin", "app": "automation"}
            ... )
        """
        # Determine client_id (use provided, or session-specific, or default)
        self._client_id = client_id if client_id is not None else self.DEFAULT_CLIENT_ID
        self._session = session
        
        # If using session and rate limiting params not provided, use session defaults
        if session:
            # Use session's rate limiting settings as defaults (can be overridden by explicit params)
            if rate_limit is False and session._rate_limit:
                rate_limit = session._rate_limit
            if rate_limit_strategy == "queue" and session._rate_limit_strategy != "queue":
                rate_limit_strategy = session._rate_limit_strategy
            if rate_limit_max_requests == 100 and session._rate_limit_max_requests != 100:
                rate_limit_max_requests = session._rate_limit_max_requests
            if rate_limit_window_seconds == 60.0 and session._rate_limit_window_seconds != 60.0:
                rate_limit_window_seconds = session._rate_limit_window_seconds
            if rate_limit_queue_size == 100 and session._rate_limit_queue_size != 100:
                rate_limit_queue_size = session._rate_limit_queue_size
            if rate_limit_queue_timeout == 30.0 and session._rate_limit_queue_timeout != 30.0:
                rate_limit_queue_timeout = session._rate_limit_queue_timeout
            if rate_limit_queue_overflow == "block" and session._rate_limit_queue_overflow != "block":
                rate_limit_queue_overflow = session._rate_limit_queue_overflow
            if circuit_breaker is False and session._circuit_breaker:
                circuit_breaker = session._circuit_breaker
            if circuit_breaker_threshold == 5 and session._circuit_breaker_threshold != 5:
                circuit_breaker_threshold = session._circuit_breaker_threshold
            if circuit_breaker_timeout == 60.0 and session._circuit_breaker_timeout != 60.0:
                circuit_breaker_timeout = session._circuit_breaker_timeout
            if circuit_breaker_half_open_calls == 3 and session._circuit_breaker_half_open_calls != 3:
                circuit_breaker_half_open_calls = session._circuit_breaker_half_open_calls
        
        # Obtain OAuth token based on auth method
        if session:
            # CloudSession mode - get token from session
            oauth_token = session.get_token(self._client_id)
            self._auth = None
            
            # Create token callback for auto-refresh before each request
            # Only if check_before_request is enabled (default: True)
            if session._check_before_request:
                def get_fresh_token() -> str:
                    return session.ensure_token_valid(self._client_id)
                
                token_callback = get_fresh_token
            else:
                token_callback = None
        elif not oauth_token:
            # Direct auth mode - create auth client
            if not api_id or not password:
                raise ValueError(
                    "Either session, oauth_token, or (api_id and password) must be provided"
                )
            
            # Auto-login to get token
            self._auth = FortiCloudAuth(
                api_id=api_id,
                password=password,
                client_id=self._client_id,
                auth_url=auth_url,
            )
            oauth_token = self._auth.get_token()
            token_callback = None
        else:
            # Pre-obtained token mode
            self._auth = None
            token_callback = None
        
        # Initialize HTTP client with OAuth authentication
        self._client = CloudHTTPClient(
            url=base_url,
            oauth_token=oauth_token,
            verify=verify,
            max_retries=max_retries,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            read_only=read_only,
            track_operations=track_operations,
            audit_handler=audit_handler,
            audit_callback=audit_callback,
            user_context=user_context,
            token_callback=token_callback,
            # NEW: Pass rate limiting parameters
            rate_limit=rate_limit,
            rate_limit_strategy=rate_limit_strategy,
            rate_limit_max_requests=rate_limit_max_requests,
            rate_limit_window_seconds=rate_limit_window_seconds,
            rate_limit_queue_size=rate_limit_queue_size,
            rate_limit_queue_timeout=rate_limit_queue_timeout,
            rate_limit_queue_overflow=rate_limit_queue_overflow,
            circuit_breaker=circuit_breaker,
            circuit_breaker_threshold=circuit_breaker_threshold,
            circuit_breaker_timeout=circuit_breaker_timeout,
            circuit_breaker_half_open_calls=circuit_breaker_half_open_calls,
        )
        
        # Token management (for session manager)
        self._refresh_token: Optional[str] = None
        self._token_created_at: Optional[float] = None  # Unix timestamp
        self._token_expires_in: Optional[int] = None    # Seconds from creation
        
        # Rate limit tracking for this client instance
        # Set limits as needed: FortiCare documented limits are 100 calls/min, 1000 calls/hour
        self._rate_stats = RateLimitStats(
            calls_per_min=rate_limit_calls_per_min,
            calls_per_5min=rate_limit_calls_per_5min,
            calls_per_hour=rate_limit_calls_per_hour,
            errors_per_min=rate_limit_errors_per_min,
            errors_per_5min=rate_limit_errors_per_5min,
            errors_per_hour=rate_limit_errors_per_hour,
        )
        
        # Initialize API endpoints
        self.api = V3API(self._client)
    
    def get_rate_limit_status(self) -> dict[str, Any]:
        """
        Get rate limit status for this FortiCare client.
        
        Returns statistics about API calls and errors for this specific
        client instance (not session-wide).
        
        Returns:
            Dictionary containing:
            - calls_last_minute: Call count in last 60 seconds
            - calls_last_hour: Call count in last 3600 seconds
            - errors_last_minute: Error count in last 60 seconds
            - errors_last_hour: Error count in last 3600 seconds
            - total_calls: Total calls since client creation
            - total_errors: Total errors since client creation
            - limits: Configured rate limits
            - within_limits: Whether client is within all configured limits
        
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> status = fcc.get_rate_limit_status()
            >>> print(f"Calls last hour: {status['calls_last_hour']}/{status['limits']['calls_per_hour']}")
            >>> if not status['within_limits']:
            ...     print("⚠️  Rate limit exceeded!")
        """
        return self._rate_stats.get_status()
    
    def get_retry_stats(self) -> dict[str, Any]:
        """
        Get retry statistics from HTTP client.
        
        Returns statistics about retry attempts, including total retries,
        reasons for retries, and per-endpoint retry counts.
        
        Returns:
            Dictionary containing:
            - total_retries: Total retry attempts
            - total_requests: Total requests made
            - successful_requests: Successful requests
            - failed_requests: Failed requests
            - retry_by_reason: Retry counts by reason
            - retry_by_endpoint: Retry counts by endpoint
            - last_retry_time: Most recent retry timestamp
        
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> stats = fcc.get_retry_stats()
            >>> print(f"Total retries: {stats['total_retries']}")
        """
        if not hasattr(self._client, "get_retry_stats"):
            return {
                "total_retries": 0,
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "retry_by_reason": {},
                "retry_by_endpoint": {},
                "last_retry_time": None,
            }
        return self._client.get_retry_stats()
    
    def get_circuit_breaker_state(self) -> dict[str, Any]:
        """
        Get current circuit breaker state.
        
        Returns the state of the circuit breaker including whether it's
        open, closed, or half-open.
        
        Returns:
            Dictionary containing:
            - state: Current state ("closed", "open", or "half_open")
            - consecutive_failures: Number of consecutive failures
            - failure_threshold: Threshold for opening circuit
            - timeout: Seconds before transitioning to half-open
            - last_failure_time: Most recent failure timestamp
        
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> state = fcc.get_circuit_breaker_state()
            >>> print(f"Circuit is {state['state']}")
        """
        if not hasattr(self._client, "get_circuit_breaker_state"):
            return {
                "state": "closed",
                "consecutive_failures": 0,
                "failure_threshold": 0,
                "timeout": 0,
                "last_failure_time": None,
            }
        return self._client.get_circuit_breaker_state()
    
    def get_health_metrics(self) -> dict[str, Any]:
        """
        Get comprehensive health metrics for HTTP client.
        
        Returns health metrics including circuit breaker state,
        retry statistics, and response time metrics.
        
        Returns:
            Dictionary containing:
            - circuit_breaker: Circuit breaker state
            - retry_stats: Retry statistics
            - adaptive_retry_enabled: Whether adaptive retry is active
            - response_times: Per-endpoint metrics (if enabled)
        
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> metrics = fcc.get_health_metrics()
            >>> print(f"Circuit state: {metrics['circuit_breaker']['state']}")
        """
        if not hasattr(self._client, "get_health_metrics"):
            return {
                "error": "Health metrics not available for this client",
                "circuit_breaker": {},
                "retry_stats": {},
                "adaptive_retry_enabled": False,
            }
        return self._client.get_health_metrics()
    
    def get_operations(self) -> list[dict[str, Any]]:
        """
        Get audit log of all tracked API operations.
        
        Returns all tracked operations (GET/POST/PUT/DELETE) in chronological order.
        Only available when track_operations=True was passed to constructor.
        
        Returns:
            List of operation dictionaries with request/response metadata
            
        Example:
            >>> fcc = FortiCare(oauth_token="...", track_operations=True)
            >>> fcc.products.list(serial_number="FGT*")
            >>> ops = fcc.get_operations()
            >>> print(f"Made {len(ops)} API calls")
        """
        if not hasattr(self._client, "get_operations"):
            return []
        return self._client.get_operations()
    
    def get_write_operations(self) -> list[dict[str, Any]]:
        """
        Get audit log of write operations only (POST/PUT/DELETE).
        
        Filters tracked operations to return only write operations, excluding GET requests.
        
        Returns:
            List of write operation dictionaries
            
        Example:
            >>> fcc = FortiCare(oauth_token="...", track_operations=True)
            >>> fcc.products.register(serial_number="FGT123", ...)
            >>> write_ops = fcc.get_write_operations()
            >>> print(f"Made {len(write_ops)} write operations")
        """
        if not hasattr(self._client, "get_write_operations"):
            return []
        return self._client.get_write_operations()
    
    def get_connection_stats(self) -> dict[str, Any]:
        """
        Get connection pool statistics.
        
        Returns:
            Dictionary with connection pool metrics (active requests, total requests, etc.)
            
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> stats = fcc.get_connection_stats()
            >>> print(f"Active requests: {stats['active_requests']}")
        """
        if not hasattr(self._client, "get_connection_stats"):
            return {
                "active_requests": 0,
                "total_requests": 0,
                "max_connections": 100,
                "max_keepalive_connections": 20,
            }
        return self._client.get_connection_stats()
    
    def inspect_last_request(self) -> Optional[dict[str, Any]]:
        """
        Get detailed information about the last HTTP request/response.
        
        Useful for debugging and understanding what was sent/received.
        
        Returns:
            Dictionary with last request details or None if no requests made
            
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> fcc.products.list()
            >>> last = fcc.inspect_last_request()
            >>> print(f"Last request took {last['response_time']}s")
        """
        if not hasattr(self._client, "inspect_last_request"):
            return None
        return self._client.inspect_last_request()
    
    def login(self, force_refresh: bool = False) -> dict[str, Any]:
        """
        Perform OAuth login and return the full authentication response.
        
        This method is useful for:
        - Explicitly logging in to see the OAuth response
        - Refreshing an expired token
        - Debugging authentication issues
        
        Note:
            If FortiCare was initialized with credentials (api_id/password),
            login happens automatically during __init__. This method allows
            you to see the response or force a token refresh.
        
        Args:
            force_refresh: Force request new token even if one is cached (default: False)
        
        Returns:
            Dictionary containing the full OAuth response with keys:
            - access_token: The OAuth bearer token
            - token_type: Token type (usually "Bearer")
            - expires_in: Token validity duration in seconds
            - scope: Token scope
            
        Raises:
            RuntimeError: If FortiCare was initialized with oauth_token (no credentials to login)
            httpx.HTTPError: If authentication request fails
        
        Example:
            >>> # Initialize with credentials
            >>> fcc = FortiCare(api_id="...", password="...")
            >>> 
            >>> # Explicitly login to see response
            >>> response = fcc.login()
            >>> print(f"Token expires in: {response['expires_in']} seconds")
            >>> 
            >>> # Force token refresh
            >>> new_response = fcc.login(force_refresh=True)
        """
        if self._auth is None:
            raise RuntimeError(
                "Cannot login: FortiCare was initialized with oauth_token. "
                "Login is only available when initialized with api_id and password."
            )
        
        # Get full OAuth response (need to modify get_token to return full response)
        import httpx
        import time
        
        logger.info(f"Performing OAuth login for client_id={self._auth.client_id}")
        
        if self._auth._token and not force_refresh:
            # Token exists but we want to return info about it
            # Since OAuth endpoint doesn't have a token info endpoint,
            # we'll return cached token info
            logger.debug("Using cached OAuth token")
            
            # Calculate time remaining if we have expiration info
            time_remaining = None
            if self._token_created_at and self._token_expires_in:
                elapsed = time.time() - self._token_created_at
                time_remaining = int(self._token_expires_in - elapsed)
            
            return {
                "access_token": self._auth._token,
                "token_type": "Bearer",
                "message": "Using cached token (use force_refresh=True to get new token)",
                "time_remaining": time_remaining,
            }
        
        # Prepare request payload
        payload = {
            "username": self._auth.api_id,
            "password": self._auth.password,
            "client_id": self._auth.client_id,
            "grant_type": "password",
        }
        
        try:
            # Request OAuth token
            with httpx.Client() as client:
                response = client.post(
                    self._auth.auth_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0,
                )
                response.raise_for_status()
            
            # Get full response
            data = response.json()
            
            # Update cached token and refresh token
            self._auth._token = data["access_token"]
            self._refresh_token = data.get("refresh_token")
            self._token_created_at = time.time()
            self._token_expires_in = data.get("expires_in")
            
            # Update client's OAuth token
            self._client._oauth_token = data["access_token"]
            
            # Close existing session so it will be recreated with new token
            if hasattr(self._client, '_session') and self._client._session is not None:
                self._client._session.close()
                self._client._session = None
            
            logger.info("Successfully obtained OAuth token")
            logger.debug(f"Token: {data['access_token'][:20]}...")
            logger.debug(f"Expires in: {data.get('expires_in')} seconds")
            
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(
                f"OAuth authentication failed: {e.response.status_code} - "
                f"{e.response.text}"
            )
            raise
        except KeyError as e:
            logger.error(f"Invalid OAuth response: missing {e}")
            raise
        except Exception as e:
            logger.error(f"OAuth token request failed: {e}")
            raise
    
    def refresh_token(self) -> dict[str, Any]:
        """
        Refresh the OAuth access token using the refresh token.
        
        This method is more efficient than login() as it uses the refresh_token
        instead of requiring username/password. The refresh token is obtained
        during the initial login and can be used to get a new access token
        without re-authenticating.
        
        Benefits:
            - Faster than full login (no password validation)
            - Extends session without re-entering credentials
            - More efficient for long-running applications
        
        Returns:
            Dictionary containing the refreshed OAuth response with keys:
            - access_token: The new OAuth bearer token
            - refresh_token: New refresh token for next refresh
            - token_type: Token type (usually "Bearer")
            - expires_in: Token validity duration in seconds
            - scope: Token scope
            - message: Status message
            - status: Status indicator
            
        Raises:
            RuntimeError: If no refresh token is available (need to login first)
            httpx.HTTPError: If token refresh request fails
        
        Example:
            >>> # Initialize and login
            >>> fcc = FortiCare(api_id="...", password="...")
            >>> 
            >>> # Get initial login response (has refresh_token)
            >>> login_resp = fcc.login(force_refresh=True)
            >>> print(f"Token expires in: {login_resp['expires_in']} seconds")
            >>> 
            >>> # Later, refresh the token (more efficient than re-login)
            >>> refresh_resp = fcc.refresh_token()
            >>> print(f"New token expires in: {refresh_resp['expires_in']} seconds")
            >>> 
            >>> # Continue using API with refreshed token
            >>> folders = fcc.api.folders.list.post()
        """
        if not self._refresh_token:
            raise RuntimeError(
                "No refresh token available. You must login first with login(force_refresh=True) "
                "to obtain a refresh token."
            )
        
        if self._auth is None:
            raise RuntimeError(
                "Cannot refresh token: FortiCare was initialized with oauth_token only. "
                "Token refresh requires initialization with api_id and password."
            )
        
        import httpx
        import time
        
        logger.info(f"Refreshing OAuth token for client_id={self._auth.client_id}")
        
        # Prepare refresh request payload
        payload = {
            "client_id": self._auth.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        
        try:
            # Request token refresh
            with httpx.Client() as client:
                response = client.post(
                    self._auth.auth_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0,
                )
                response.raise_for_status()
            
            # Get full response
            data = response.json()
            
            # Update cached tokens and timestamp
            self._auth._token = data["access_token"]
            self._refresh_token = data.get("refresh_token", self._refresh_token)
            self._token_created_at = time.time()
            self._token_expires_in = data.get("expires_in")
            
            # Update client's OAuth token
            self._client._oauth_token = data["access_token"]
            
            # Close existing session so it will be recreated with new token
            if hasattr(self._client, '_session') and self._client._session is not None:
                self._client._session.close()
                self._client._session = None
            
            logger.info("Successfully refreshed OAuth token")
            logger.debug(f"New token: {data['access_token'][:20]}...")
            logger.debug(f"Expires in: {data.get('expires_in')} seconds")
            
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(
                f"OAuth token refresh failed: {e.response.status_code} - "
                f"{e.response.text}"
            )
            # Clear invalid refresh token
            self._refresh_token = None
            raise
        except KeyError as e:
            logger.error(f"Invalid OAuth refresh response: missing {e}")
            raise
        except Exception as e:
            logger.error(f"OAuth token refresh request failed: {e}")
            raise
    
    def get_token_time_remaining(self) -> Optional[int]:
        """
        Get the number of seconds remaining until the access token expires.
        
        Returns:
            Number of seconds until token expires, or None if expiration unknown
            
        Example:
            >>> fcc = FortiCare(api_id="...", password="...")
            >>> remaining = fcc.get_token_time_remaining()
            >>> if remaining and remaining < 300:
            ...     print("Token expires in less than 5 minutes!")
            ...     fcc.refresh_token()
        """
        if not self._token_created_at or not self._token_expires_in:
            return None
        
        import time
        elapsed = time.time() - self._token_created_at
        remaining = int(self._token_expires_in - elapsed)
        return max(0, remaining)  # Never return negative
    
    def is_token_expired(self, buffer_seconds: int = 0) -> bool:
        """
        Check if the access token is expired or will expire soon.
        
        Args:
            buffer_seconds: Consider token expired if it expires within this many seconds (default: 0)
                           Use a buffer (e.g., 300 for 5 minutes) for proactive refresh
        
        Returns:
            True if token is expired or will expire within buffer_seconds, False otherwise
            If expiration time is unknown, returns False (assumes token is valid)
            
        Example:
            >>> fcc = FortiCare(api_id="...", password="...")
            >>> 
            >>> # Check if token is expired
            >>> if fcc.is_token_expired():
            ...     fcc.refresh_token()
            >>> 
            >>> # Proactive refresh (5 minutes before expiry)
            >>> if fcc.is_token_expired(buffer_seconds=300):
            ...     print("Token expiring soon, refreshing...")
            ...     fcc.refresh_token()
        """
        remaining = self.get_token_time_remaining()
        if remaining is None:
            return False  # Unknown expiration, assume valid
        return remaining <= buffer_seconds
    
    def get_token_info(self) -> dict[str, Any]:
        """
        Get comprehensive information about the current access token.
        
        Returns:
            Dictionary containing:
            - has_token: Whether a token exists
            - has_refresh_token: Whether a refresh token exists
            - created_at: Token creation timestamp (Unix time)
            - expires_in: Original expiration duration in seconds
            - time_remaining: Seconds until token expires
            - is_expired: Whether token is currently expired
            - expires_soon: Whether token expires within 5 minutes
            
        Example:
            >>> fcc = FortiCare(api_id="...", password="...")
            >>> info = fcc.get_token_info()
            >>> print(f"Token valid for {info['time_remaining']} more seconds")
            >>> if info['expires_soon']:
            ...     fcc.refresh_token()
        """
        import time
        from datetime import datetime, timezone
        
        info: dict[str, Any] = {
            "has_token": self._auth is not None and self._auth._token is not None,
            "has_refresh_token": self._refresh_token is not None,
            "created_at": self._token_created_at,
            "created_at_iso": None,
            "expires_in": self._token_expires_in,
            "time_remaining": self.get_token_time_remaining(),
            "is_expired": self.is_token_expired(),
            "expires_soon": self.is_token_expired(buffer_seconds=300),  # 5 minutes
            "expires_at": None,
            "expires_at_iso": None,
        }
        
        # Add human-readable timestamp
        if self._token_created_at:
            dt = datetime.fromtimestamp(self._token_created_at, tz=timezone.utc)
            info["created_at_iso"] = dt.isoformat()
        
        # Add expiration timestamp
        if self._token_created_at and self._token_expires_in:
            expires_at = self._token_created_at + self._token_expires_in
            dt = datetime.fromtimestamp(expires_at, tz=timezone.utc)
            info["expires_at"] = expires_at
            info["expires_at_iso"] = dt.isoformat()
        
        return info
    
    def logout(self) -> None:
        """
        Close the HTTP session and clean up resources.
        
        Note:
            OAuth token revocation should be handled separately.
            This method only closes the HTTP connection.
        
        Example:
            >>> fcc = FortiCare(oauth_token="...")
            >>> # ... use the client ...
            >>> fcc.logout()
        """
        self._client.logout()
    
    def __enter__(self) -> FortiCare:
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - ensures session is closed."""
        self.logout()
    
    def __repr__(self) -> str:
        """String representation."""
        return f"FortiCare(base_url='{self._client._url}')"

