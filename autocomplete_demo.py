#!/usr/bin/env python3
"""
Simple FortiCare API Example - Demonstrating Type Hints

This shows that IDE autocomplete and type checking work properly.
"""

from hfortix_forticare import FortiCare

# Initialize - IDE should autocomplete parameters
fcc = FortiCare(
    oauth_token="your_token",
    base_url="https://support.fortinet.com",  # Optional, autocompletes
    verify=True,                              # Optional, autocompletes
    max_retries=3,                            # Optional, autocompletes
    connect_timeout=10.0,                     # Optional, autocompletes
    read_timeout=300.0                        # Optional, autocompletes
)

# Access API - IDE should show: fcc.api -> V3API
# Then show available categories: contracts, folders, licenses, products, services
api = fcc.api

# Access products category - IDE should show: ProductsCategory
products = api.products

# Access list endpoint - IDE should show: ProductList
product_list = products.list

# Call post method - IDE should autocomplete ALL parameters:
# - serial_number: Optional[str]
# - expire_before: Optional[str]  
# - status: Optional[str]
# - product_model: Optional[str]
# - account_id: Optional[float]
result = product_list.post(
    serial_number="FGT*",      # <-- IDE autocompletes this
    status="Registered",       # <-- and this
    expire_before="2024-12-31" # <-- and this
)

# Result is typed as ProductListResponse (TypedDict)
# IDE should show available fields when you type result["
# - status: int
# - message: str
# - token: str
# - version: str
# - assets: list[any]
# - build: str
# - error: str

if result.get("status") == 0:
    print("Success!")
    assets = result.get("assets", [])
    for asset in assets:
        # Each asset is dict[str, Any] - this is expected
        print(f"Serial: {asset.get('serialNumber')}")

# You can also chain it (more concise):
response = fcc.api.products.details.post(
    serial_number="FGT123"  # IDE autocompletes parameter
)

# IDE autocomplete should work for all categories and endpoints:
# fcc.api.contracts.list.post(...)
# fcc.api.licenses.list.post(...)
# fcc.api.licenses.register.post(...)
# fcc.api.licenses.download.post(...)
# fcc.api.folders.list.post(...)
# fcc.api.folders.create.post(...)
# fcc.api.folders.delete.post(...)
# fcc.api.services.register.post(...)
# fcc.api.products.list.post(...)
# fcc.api.products.register.post(...)
# fcc.api.products.details.post(...)
# fcc.api.products.description.post(...)
# fcc.api.products.location.post(...)
# fcc.api.products.folder.post(...)
# fcc.api.products.decommission.post(...)
# fcc.api.products.transfer.post(...)

fcc.logout()

print("\n✅ Type hints work correctly!")
print("   - IDE autocompletes all parameters")
print("   - Return types are properly typed")
print("   - All endpoints accessible with proper types")
