API Reference
=============

FortiCare Client
----------------

.. autoclass:: hfortix_forticare.FortiCare
   :members:
   :undoc-members:
   :show-inheritance:

API Endpoints
-------------

The FortiCare API is structured as:

.. code-block:: python

   fc.api.
     ├── products.
     │   ├── list          # List products with entitlements
     │   ├── register      # Register products and contracts
     │   ├── details       # Get product details
     │   ├── description   # Update product description
     │   ├── location      # Update product location
     │   ├── folder        # Update product folder
     │   ├── decommission  # Decommission products
     │   └── transfer      # Transfer products
     ├── licenses.
     │   ├── list          # List licenses
     │   ├── register      # Register license
     │   └── download      # Download VM license file
     ├── contracts.
     │   └── list          # List contracts
     ├── folders.
     │   ├── list          # List folders
     │   ├── create        # Create folder
     │   └── delete        # Delete folder
     └── services.
         └── register      # Register subscription service

Response Models
---------------

.. autoclass:: hfortix_forticare.FortiCareResponse
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: hfortix_forticare.FortiCareObject
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: hfortix_forticare.FortiCareList
   :members:
   :undoc-members:
   :show-inheritance:

Type Definitions
----------------

.. autoclass:: hfortix_forticare.Product
   :members:
   :undoc-members:
   :show-inheritance:
