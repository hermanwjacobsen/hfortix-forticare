# hfortix-forticare

Python SDK for the Fortinet FortiCare Asset Management V3 API.

## Overview

`hfortix-forticare` provides a fully typed Python interface to the FortiCare
Asset Management API, enabling programmatic access to:

- **Product Management**: Register, list, update, and decommission products
- **License Management**: Register, list, and download licenses
- **Contract Management**: View contract information
- **Folder Management**: Organize assets into folders
- **Service Management**: Register subscription services

## Features

- **Fully Typed** — `py.typed` + `.pyi` stubs (PEP 561) for IDE
  auto-completion and static type checking
- **OAuth 2.0** — Built-in FortiCloud OAuth token acquisition, refresh, and
  lifecycle management
- **Shared Sessions** — `CloudSession` support for sharing credentials with
  other FortiCloud clients (e.g. `hfortix-fortiztp`)
- **Resilience** — Optional rate limiting and circuit breaker (opt-in),
  automatic retries with backoff
- **Auditing** — Optional operation tracking and audit logging

## Installation

```bash
pip install hfortix-forticare
```

## Quick Start

### 1. Authentication

You have multiple options for authentication:

#### Option A: CloudSession (Recommended for Multi-Service)

```python
from hfortix_core.session import CloudSession
from hfortix_forticare import FortiCare

# CloudSession manages tokens for multiple services
with CloudSession(api_id="your_api_id", password="your_password") as session:
    fc = FortiCare(session=session)  # Auto-uses "assetmanagement" client_id
    products = fc.api.products.list.post()
    # Token is automatically managed and shared efficiently
```

CloudSession can also configure rate limiting once for every client that
uses it:

```python
from hfortix_core.session import CloudSession
from hfortix_forticare import FortiCare

session = CloudSession(
    api_id="your_api_id",
    password="your_password",
    # Global rate limiting - inherited by all clients
    rate_limit=True,
    rate_limit_max_requests=20,       # 20 requests per window
    rate_limit_window_seconds=60.0,
    circuit_breaker=True,
)

fc = FortiCare(session=session)  # Inherits 20 req/min

# Or override for a specific client
fc_fast = FortiCare(
    session=session,
    rate_limit_max_requests=50,  # Override session's 20 req/min
)
```

#### Option B: Auto-Login with Credentials

```python
from hfortix_forticare import FortiCare

# Auto-login with API credentials
fcc = FortiCare(
    api_id="your_api_id",
    password="your_password",
)
# Token is automatically obtained and managed
```

#### Option C: Use a Pre-Obtained OAuth Token

```python
# Get token from the FortiCloud OAuth endpoint first:
# https://customerapiauth.fortinet.com/api/v1/oauth/token/

fcc = FortiCare(oauth_token="your_oauth_token_here")
```

### 2. Use the API

> **Wildcard note:** `serial_number` filters use SQL `LIKE` wildcards —
> use `%` (e.g. `"FGT%"`), **not** `*`. It defaults to `"%"` (all products).

```python
# List products with entitlements
products = fcc.api.products.list.post(
    serial_number="FGT%",
    status="Registered",
)

# Get product details
details = fcc.api.products.details.post(
    serial_number="FGT90D1234567890",
)

# Register a product
result = fcc.api.products.register.post(
    registration_units=[
        {
            "serialNumber": "FGT90D1234567890",
            "description": "My FortiGate",
            # ... other fields
        }
    ]
)

# List contracts
contracts = fcc.api.contracts.list.post()

# List licenses
licenses = fcc.api.licenses.list.post()

# Manage folders
folders = fcc.api.folders.list.post()

# Always clean up when done
fcc.logout()
```

## API Structure

The SDK mirrors the FortiCare Asset Management V3 API structure:

```
fcc.api.
  ├── products.
  │   ├── list          - List products with entitlements
  │   ├── register      - Register products and contracts
  │   ├── details       - Get product details
  │   ├── description   - Update product description
  │   ├── location      - Update product location
  │   ├── folder        - Update product folder
  │   ├── decommission  - Decommission products
  │   └── transfer      - Transfer products between accounts
  ├── licenses.
  │   ├── list          - List licenses
  │   ├── register      - Register a license
  │   └── download      - Download VM license file
  ├── contracts.
  │   └── list          - List contracts
  ├── folders.
  │   ├── list          - List asset folders
  │   ├── create        - Create new folder
  │   └── delete        - Delete folder
  └── services.
      └── register      - Register subscription service
```

## Responses

Every endpoint returns a `FortiCareResponse` object with attribute access
(responses are **not** subscriptable — use attributes or `.get()`):

```python
response = fcc.api.products.list.post(serial_number="FGT%")

response.status            # API status code (0 = success)
response.message           # Error message (empty on success)
response.http_status_code  # HTTP status code (200, 404, ...)
response.response_time     # Request duration in seconds
response.raw               # Full response as a plain dict
response.get("assets", []) # Dict-style access with default

# List responses expose typed collections
for asset in response.assets:
    print(asset.serialNumber, asset.productModel)
```

## Rate Limits

The FortiCare Asset Management API enforces the following limits server-side:

- **100 calls per minute**
- **1000 calls per hour**
- **10 errors per hour**
- **Batch operations**: Max 10 units, max 5 errors per batch

### Rate Limit Enforcement (opt-in)

Client-side enforcement is **disabled by default**. Enable it with
`rate_limit=True` (token bucket with queue support):

```python
from hfortix_forticare import FortiCare

fcc = FortiCare(
    api_id="your_api_id",
    password="your_password",
    rate_limit=True,
    rate_limit_max_requests=100,      # FortiCare: 100/min
    rate_limit_window_seconds=60.0,   # 60 second window
    rate_limit_strategy="queue",      # Queue excess requests
    rate_limit_queue_size=50,         # Max 50 queued requests
)
```

**Rate limiting / circuit breaker parameters:**

- `rate_limit: bool = False` — Enable/disable rate limiting
- `rate_limit_strategy: str = "queue"` — Strategy: `queue`, `drop`, or `raise`
- `rate_limit_max_requests: int = 100` — Max requests per window
- `rate_limit_window_seconds: float = 60.0` — Time window in seconds
- `rate_limit_queue_size: int = 100` — Max queued requests
- `rate_limit_queue_timeout: float = 30.0` — Max wait time in queue
- `rate_limit_queue_overflow: str = "block"` — Overflow: `block`, `drop`, or `raise`
- `circuit_breaker: bool = False` — Enable circuit breaker
- `circuit_breaker_threshold: int = 5` — Failures before opening
- `circuit_breaker_timeout: float = 60.0` — Seconds before retry
- `circuit_breaker_half_open_calls: int = 3` — Test calls in half-open state

### Rate Limit Tracking (monitoring only)

Track your API usage to stay within limits — these counters are
**informational only** and never block requests:

```python
from hfortix_forticare import FortiCare

# Configure custom limits (all optional, default to None = no limit)
fcc = FortiCare(
    api_id="...",
    password="...",
    rate_limit_calls_per_min=100,      # FortiCare: 100/min
    rate_limit_calls_per_hour=1000,    # FortiCare: 1000/hour
    rate_limit_errors_per_hour=10,     # FortiCare: 10 errors/hour
)

products = fcc.api.products.list.post()

status = fcc.get_rate_limit_status()
print(f"Calls last min: {status['calls_last_min']}")
print(f"Calls last hour: {status['calls_last_hour']}")
print(f"Errors last hour: {status['errors_last_hour']}")
print(f"Within limits: {status['within_limits']}")
```

## Error Handling

API-level errors are reported in the response body (`.status != 0`).
HTTP and network failures raise `httpx` exceptions; the opt-in rate
limiter and circuit breaker raise `hfortix_core.exceptions` types:

```python
import httpx

from hfortix_core.exceptions import (
    CircuitBreakerOpenError,
    RateLimitExceededError,
)

try:
    result = fcc.api.products.list.post(serial_number="FGT%")

    if result.status == 0:
        print("Success!")
    else:
        print(f"API Error: {result.message}")

except httpx.HTTPStatusError as e:
    print(f"HTTP Error: {e.response.status_code}")
except httpx.TimeoutException:
    print("Request timed out")
except httpx.RequestError as e:
    print(f"Network error: {e}")
except CircuitBreakerOpenError:
    print("Circuit breaker is open")  # only with circuit_breaker=True
except RateLimitExceededError:
    print("Rate limited")  # only with rate_limit=True, strategy="raise"
```

## Context Manager

Use as a context manager for automatic cleanup:

```python
with FortiCare(oauth_token="...") as fcc:
    products = fcc.api.products.list.post()
    # ... use the client ...
# Automatically logged out
```

## Configuration

```python
fcc = FortiCare(
    oauth_token="your_token",
    # Default base URL:
    base_url="https://support.fortinet.com/ES/api/registration/v3",
    verify=True,           # SSL verification
    max_retries=3,         # Retry attempts
    connect_timeout=10.0,  # Connection timeout (seconds)
    read_timeout=300.0,    # Read timeout (seconds)
)
```

## OAuth Token Management

The SDK provides OAuth token lifecycle management for long-running
applications (available when initialized with `api_id`/`password`):

### View Login Response

```python
fcc = FortiCare(api_id="...", password="...")
response = fcc.login(force_refresh=True)

print(f"Access Token: {response['access_token']}")
print(f"Refresh Token: {response['refresh_token']}")
print(f"Expires In: {response['expires_in']} seconds")
```

### Refresh Token

```python
# Efficiently refresh token without re-entering credentials
# (requires a prior login(force_refresh=True) to obtain a refresh token)
refresh_response = fcc.refresh_token()
print(f"New token expires in: {refresh_response['expires_in']}s")
```

### Track Token Expiration

```python
# Check time remaining
remaining = fcc.get_token_time_remaining()
print(f"Token valid for {remaining} more seconds")

# Check if expired or expiring soon
if fcc.is_token_expired(buffer_seconds=300):  # 5 min buffer
    print("Token expiring soon, refreshing...")
    fcc.refresh_token()

# Get comprehensive token info
info = fcc.get_token_info()
print(f"Created: {info['created_at_iso']}")
print(f"Expires: {info['expires_at_iso']}")
print(f"Time Remaining: {info['time_remaining']}s")
print(f"Expires Soon: {info['expires_soon']}")
```

## Package Structure

```text
hfortix_forticare/
├── __init__.py           # Main FortiCare client
├── models.py             # FortiCareResponse and typed wrappers
├── types.py              # TypedDict definitions
└── api/
    └── v3/
        ├── __init__.py   # V3API class
        ├── products/     # Product endpoints
        ├── licenses/     # License endpoints
        ├── contracts/    # Contract endpoints
        ├── folders/      # Folder endpoints
        └── services/     # Service endpoints
```

## Requirements

- Python 3.9+
- [httpx](https://www.python-httpx.org/)
- [hfortix-core](https://github.com/hermanwjacobsen/hfortix-core)

## License

Proprietary — free to use, but may not be resold or redistributed as a
standalone product. See [LICENSE](./LICENSE) for the full terms.

Copyright (c) 2025 Herman W. Jacobsen

## Links

- [FortiCare API Documentation](https://docs.fortinet.com/document/forticloud/latest/asset-management-api/)
- [FortiCloud IAM Portal](https://support.fortinet.com/)
- [hfortix-core](https://github.com/hermanwjacobsen/hfortix-core)
- [hfortix-fortiztp](https://github.com/hermanwjacobsen/hfortix-fortiztp)
