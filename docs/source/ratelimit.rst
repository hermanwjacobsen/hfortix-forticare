Rate Limit Tracking
===================

FortiCare includes built-in rate limit tracking to help you monitor API usage and stay within limits.

Overview
--------

FortiCare API enforces:

* **100 calls per minute**
* **1000 calls per hour**
* **10 errors per hour**

The tracking system monitors your usage across multiple time windows but does **not enforce** limits.

Basic Usage
-----------

.. code-block:: python

   from hfortix_forticare import FortiCare

   # Configure rate limits (optional, defaults to None)
   fc = FortiCare(
       api_id="...",
       password="...",
       rate_limit_calls_per_min=100,
       rate_limit_calls_per_5min=500,
       rate_limit_calls_per_hour=1000,
       rate_limit_errors_per_hour=10
   )

   # Make API calls
   products = fc.api.products.list.post()

   # Check status
   status = fc.get_rate_limit_status()

Status Response
---------------

.. code-block:: python

   {
       "calls_last_min": 45,       # Calls in last 60 seconds
       "calls_last_5min": 180,     # Calls in last 300 seconds
       "calls_last_hour": 523,     # Calls in last 3600 seconds
       "errors_last_min": 0,       # Errors in last 60 seconds
       "errors_last_5min": 1,      # Errors in last 300 seconds
       "errors_last_hour": 2,      # Errors in last 3600 seconds
       "total_calls": 1247,        # Total since client creation
       "total_errors": 5,          # Total errors
       "limits": {                 # Configured limits
           "calls_per_min": 100,
           "calls_per_5min": 500,
           "calls_per_hour": 1000,
           "errors_per_min": None,
           "errors_per_5min": None,
           "errors_per_hour": 10
       },
       "within_limits": True       # Whether within all limits
   }

Monitoring Example
------------------

.. code-block:: python

   fc = FortiCare(
       api_id="...",
       password="...",
       rate_limit_calls_per_min=100,
       rate_limit_calls_per_hour=1000
   )

   # Batch operation
   for serial in serial_numbers:
       # Check before calling
       status = fc.get_rate_limit_status()
       
       if not status['within_limits']:
           print(f"Approaching limits: {status['calls_last_hour']}/1000")
           time.sleep(60)  # Wait before continuing
       
       # Make API call
       fc.api.products.details.post(serial_number=serial)

Session-Wide Tracking
---------------------

When using CloudSession, you can track usage across all services:

.. code-block:: python

   from hfortix_core.session import CloudSession
   from hfortix_forticare import FortiCare
   from hfortix_fortiztp import FortiZTP

   with CloudSession(api_id="...", password="...") as session:
       fc = FortiCare(session=session)
       fz = FortiZTP(session=session)
       
       # Per-client stats
       fc_status = fc.get_rate_limit_status()
       fz_status = fz.get_rate_limit_status()
       
       # Session-wide stats (all services combined)
       session_status = session.get_rate_limit_status()

Implementation
--------------

* **Efficient tracking**: Uses ``deque`` with sliding windows
* **Multiple time windows**: Minute, 5 minutes, hour
* **No enforcement**: Informational only
* **Configurable**: Set custom limits or leave as None

See Also
--------

* :doc:`session` - CloudSession integration
* hfortix-core rate limiting documentation
