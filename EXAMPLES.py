#!/usr/bin/env python3
"""
FortiCare Asset Management API - Example Usage

This script demonstrates how to use the generated FortiCare Python SDK.
"""

from hfortix_forticare import FortiCare

# Initialize FortiCare client with OAuth token
fcc = FortiCare(
    oauth_token="your_oauth_token_here",
    base_url="https://support.fortinet.com"
)

# Example 1: List products with entitlements
print("Example 1: List products")
print("-" * 60)
try:
    # NOTE: Use % for wildcards (SQL LIKE syntax), not *
    products = fcc.api.products.list.post(
        serial_number="FGT%",  # Search pattern - all FortiGate devices
        status="Registered"
    )
    print(f"Status: {products.get('status')}")
    print(f"Message: {products.get('message')}")
    print(f"Products found: {len(products.get('assets', []))}")
except Exception as e:
    print(f"Error: {e}")

print()

# Example 2: Get product details
print("Example 2: Get product details")
print("-" * 60)
try:
    details = fcc.api.products.details.post(
        serial_number="FGT90D1234567890"
    )
    print(f"Status: {details.get('status')}")
    if details.get('status') == 0:
        asset = details.get('asset', {})
        print(f"Serial: {asset.serialNumber}")
        print(f"Model: {asset.productModel}")
except Exception as e:
    print(f"Error: {e}")

print()

# Example 3: List contracts
print("Example 3: List contracts")
print("-" * 60)
try:
    contracts = fcc.api.contracts.list.post()
    print(f"Status: {contracts.get('status')}")
    print(f"Contracts found: {len(contracts.get('contracts', []))}")
except Exception as e:
    print(f"Error: {e}")

print()

# Example 4: List licenses
print("Example 4: List licenses")
print("-" * 60)
try:
    licenses = fcc.api.licenses.list.post()
    print(f"Status: {licenses.get('status')}")
    print(f"Licenses found: {len(licenses.get('licenses', []))}")
except Exception as e:
    print(f"Error: {e}")

print()

# Example 5: List folders
print("Example 5: List folders")
print("-" * 60)
try:
    folders = fcc.api.folders.list.post()
    print(f"Status: {folders.get('status')}")
    if folders.get('status') == 0:
        folder_list = folders.get('folders', [])
        print(f"Folders found: {len(folder_list)}")
        for folder in folder_list[:3]:  # Show first 3
            print(f"  - {folder.get('folderPath')}")
except Exception as e:
    print(f"Error: {e}")

# Clean up
fcc.logout()

print()
print("=" * 60)
print("All examples completed!")
print("=" * 60)
