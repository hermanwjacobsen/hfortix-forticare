#!/usr/bin/env python3
"""
Type Checking Test for FortiCare API

This file verifies that type hints are properly working.
Run with: pyright test_types.py
"""

from hfortix_forticare import FortiCare

# Initialize client - should show proper type hints
fcc = FortiCare(oauth_token="test_token")

# Test: api attribute should be typed as V3API
reveal_type(fcc.api)  # Should show: Type of "fcc.api" is "V3API"

# Test: products should be typed as ProductsCategory  
reveal_type(fcc.api.products)  # Should show: Type of "fcc.api.products" is "ProductsCategory"

# Test: list should be typed as ProductList
reveal_type(fcc.api.products.list)  # Should show: Type of "fcc.api.products.list" is "ProductList"

# Test: post method should show proper signature
reveal_type(fcc.api.products.list.post)  # Should show the full method signature

# Test: Calling post should show return type
result = fcc.api.products.list.post(
    serial_number="FGT*",  # Should show type: str | None
    status="Registered"    # Should show type: str | None
)

# Result should be typed as ProductListResponse
reveal_type(result)  # Should show: Type of "result" is "ProductListResponse"

# Accessing response fields should work
status_code = result["status"]  # Should be typed as int
message = result["message"]     # Should be typed as str
assets = result["assets"]       # Should be typed as list[any]



# Test other endpoints
contracts = fcc.api.contracts.list.post()
reveal_type(contracts)  # Should show: Type of "contracts" is "ContractListResponse"

licenses = fcc.api.licenses.list.post()
reveal_type(licenses)  # Should show: Type of "licenses" is "LicenseListResponse"

folders = fcc.api.folders.list.post()
reveal_type(folders)  # Should show: Type of "folders" is "FolderListResponse"

# Test with parameters
product_details = fcc.api.products.details.post(
    serial_number="FGT123"  # Should show this parameter is required/optional with correct type
)
reveal_type(product_details)  # Should show: Type is "ProductDetailsResponse"

print("Type checking test complete!")
print("If you see proper types revealed above, the type hints are working correctly.")
