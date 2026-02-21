HFortix-FortiCare Documentation
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   quickstart
   session
   ratelimit
   api_reference

Installation
------------

.. code-block:: bash

   pip install hfortix-forticare

Quick Start
-----------

.. code-block:: python

   from hfortix_forticare import FortiCare

   # Auto-login with credentials
   fc = FortiCare(
       api_id="your_api_id",
       password="your_password"
   )

   # List products
   products = fc.api.products.list.post()

   # Clean up
   fc.logout()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
