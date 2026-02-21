CloudSession Integration
========================

FortiCare integrates seamlessly with CloudSession for efficient multi-service OAuth management.

Basic Usage
-----------

.. code-block:: python

   from hfortix_core.session import CloudSession
   from hfortix_forticare import FortiCare

   # CloudSession manages tokens
   with CloudSession(api_id="...", password="...") as session:
       fc = FortiCare(session=session)  # Auto-uses "assetmanagement" client_id
       products = fc.api.products.list.post()

Multi-Service Example
---------------------

.. code-block:: python

   from hfortix_core.session import CloudSession
   from hfortix_forticare import FortiCare
   from hfortix_fortiztp import FortiZTP

   with CloudSession(api_id="...", password="...") as session:
       fc = FortiCare(session=session)    # Uses "assetmanagement"
       fz = FortiZTP(session=session)     # Uses "fortiztp"
       
       # Both share the session, each with their own token
       products = fc.api.products.list.post()
       devices = fz.devices.get()

Override Client ID
------------------

.. code-block:: python

   # Use different client_id for specialized access
   with CloudSession(api_id="...", password="...") as session:
       fc_standard = FortiCare(session=session)                      # "assetmanagement"
       fc_elite = FortiCare(session=session, client_id="fcelite")   # "fcelite"

Auto-Refresh
------------

.. code-block:: python

   # Enable background token refresh
   session = CloudSession(
       api_id="...",
       password="...",
       auto_refresh=True,
       refresh_buffer_seconds=300  # Refresh 5 min before expiry
   )
   
   fc = FortiCare(session=session)
   # Tokens refresh automatically
   
   # Don't forget to close
   session.close()

Benefits
--------

* **Token sharing**: Multiple clients with same client_id share tokens
* **Automatic refresh**: Tokens stay valid without manual intervention
* **Thread-safe**: Concurrent access from multiple services
* **Clean code**: Context manager handles cleanup automatically

See Also
--------

* :doc:`ratelimit` - Rate limit tracking
* hfortix-core CloudSession documentation
