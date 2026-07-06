Quick Start
===========

Installation
------------

.. code-block:: bash

   pip install hfortix-forticare

Basic Usage
-----------

CloudSession (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hfortix_core.session import CloudSession
   from hfortix_forticare import FortiCare

   # Multi-service token management
   with CloudSession(api_id="your_api_id", password="your_password") as session:
       fc = FortiCare(session=session)
       products = fc.api.products.list.post()

Auto-Login
~~~~~~~~~~

.. code-block:: python

   from hfortix_forticare import FortiCare

   # Automatic token management
   fc = FortiCare(
       api_id="your_api_id",
       password="your_password"
   )

   # Use the API
   products = fc.api.products.list.post()

   # Clean up
   fc.logout()

Pre-Obtained Token
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hfortix_forticare import FortiCare

   # Use existing OAuth token
   fc = FortiCare(oauth_token="your_token_here")

Common Operations
-----------------

List Products
~~~~~~~~~~~~~

.. code-block:: python

   # List all products
   products = fc.api.products.list.post()

   # Filter by serial number (SQL LIKE wildcards: % not *)
   products = fc.api.products.list.post(
       serial_number="FGT%"
   )

   # Filter by status
   products = fc.api.products.list.post(
       status="Registered"
   )

Get Product Details
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   details = fc.api.products.details.post(
       serial_number="FGT90D1234567890"
   )

Register Product
~~~~~~~~~~~~~~~~

.. code-block:: python

   result = fc.api.products.register.post(
       registration_units=[
           {
               "serialNumber": "FGT90D1234567890",
               "description": "My FortiGate",
               "isGovernment": False
           }
       ]
   )

List Licenses
~~~~~~~~~~~~~

.. code-block:: python

   licenses = fc.api.licenses.list.post()

Download License
~~~~~~~~~~~~~~~~

.. code-block:: python

   license_file = fc.api.licenses.download.post(
       serial_number="FGVMXXXXXXXXXXXX"
   )

Manage Folders
~~~~~~~~~~~~~~

.. code-block:: python

   # List folders
   folders = fc.api.folders.list.post()

   # Create folder
   result = fc.api.folders.create.post(
       folder_name="Production",
       parent_folder_id=0
   )

Rate Limit Tracking
-------------------

.. code-block:: python

   # Configure rate limits
   fc = FortiCare(
       api_id="...",
       password="...",
       rate_limit_calls_per_min=100,
       rate_limit_calls_per_hour=1000,
       rate_limit_errors_per_hour=10
   )

   # Make API calls
   products = fc.api.products.list.post()

   # Check status
   status = fc.get_rate_limit_status()
   print(f"Calls: {status['calls_last_hour']}/{status['limits']['calls_per_hour']}")
   print(f"Within limits: {status['within_limits']}")

Error Handling
--------------

API-level errors are reported in the response body (``.status != 0``).
Responses are not subscriptable — use attribute access. HTTP and network
failures raise ``httpx`` exceptions; the opt-in rate limiter and circuit
breaker raise ``hfortix_core.exceptions`` types:

.. code-block:: python

   import httpx

   from hfortix_core.exceptions import (
       CircuitBreakerOpenError,
       RateLimitExceededError,
   )

   try:
       result = fc.api.products.list.post(serial_number="FGT%")

       if result.status == 0:
           print("Success!")
       else:
           print(f"API Error: {result.message}")

   except httpx.HTTPStatusError as e:
       print(f"HTTP Error: {e.response.status_code}")
   except httpx.RequestError as e:
       print(f"Network error: {e}")
   except CircuitBreakerOpenError:
       print("Circuit breaker is open")  # only with circuit_breaker=True
   except RateLimitExceededError:
       print("Rate limited")  # only with rate_limit=True, strategy="raise"
