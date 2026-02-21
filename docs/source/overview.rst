Overview
========

**HFortix-FortiCare** provides a fully typed Python SDK for the Fortinet FortiCare Asset Management V3 API.

Key Features
------------

**CloudSession Support**
   Integrate with CloudSession for efficient multi-service OAuth token management.

**Rate Limit Tracking**
   Monitor API usage across multiple time windows (last minute, 5 minutes, hour).

**Fully Typed API**
   Complete type hints with TypedDict for all requests and responses.

**Auto-completion**
   IDE auto-completion for all API parameters and return values.

**OAuth 2.0**
   Built-in OAuth Bearer token authentication with automatic token management.

**Modern HTTP**
   HTTP/2 support via httpx for optimal performance.

What You Can Do
---------------

* **Product Management**: Register, list, update, and decommission products
* **License Management**: Register, list, and download licenses
* **Contract Management**: View contract information
* **Folder Management**: Organize assets into folders
* **Service Management**: Register subscription services

API Coverage
------------

The SDK provides access to all FortiCare Asset Management V3 endpoints:

* **Products**: List, register, details, update, decommission, transfer
* **Licenses**: List, register, download
* **Contracts**: List contracts
* **Folders**: List, create, delete folders
* **Services**: Register subscription services

Authentication Options
---------------------

You have multiple ways to authenticate:

1. **CloudSession** (recommended for multi-service)
2. **Auto-login** with API credentials
3. **Pre-obtained OAuth token**

Rate Limits
-----------

FortiCare enforces the following limits:

* **100 calls per minute**
* **1000 calls per hour**
* **10 errors per hour**
* **Batch operations**: Max 10 units, max 5 errors per batch

Use the built-in rate limit tracking to monitor your usage.
