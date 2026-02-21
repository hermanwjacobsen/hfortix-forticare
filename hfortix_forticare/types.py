"""
Type definitions for FortiCare API response objects.

These TypedDicts provide type hints for common response structures
from the FortiCare Asset Management API.
"""

from typing import TypedDict, Any


class LocationInfo(TypedDict, total=False):
    """Location information for a product."""
    addressId: str
    company: str
    address: str
    city: str
    stateOrProvince: str
    countryCode: str
    postalCode: str
    email: str
    phone: str
    fax: str


class AssetDetailsInfo(TypedDict, total=False):
    """Detailed asset information from products/details endpoint."""
    productModel: str  # Product model description
    productModelEoR: str  # Product model EoR date
    productModelEoS: str  # Product model EoS date
    serialNumber: str  # Product serial number
    isDecommissioned: bool  # Whether the unit has been decommissioned
    registrationDate: str  # Product registration date (ISO 8601)
    assetGroups: list[Any]  # Asset groups
    contracts: list[Any]  # Contracts
    folderId: int  # Asset folder id
    folderPath: str  # Asset folder path
    description: str  # Product description
    partner: str  # Product associated partner name
    license: list[Any]  # Product associated license information
    entitlements: list[Any]  # Product current support coverage info
    location: LocationInfo  # Location information
    warrantySupports: list[Any]  # Warranty supports
    warrantyTypeName: str  # Warranty type
    licenseKeys: list[Any]  # License key information
    accountId: int  # Account ID


class AssetInfo(TypedDict, total=False):
    """Asset/Product information from FortiCare API."""
    
    serialNumber: str  # Serial number
    accountId: int  # Account ID
    folderId: int  # Asset folder ID
    folderPath: str  # Asset folder path
    registrationDate: str  # Registration date (ISO 8601)
    description: str  # Product description
    isDecommissioned: bool  # Whether unit is decommissioned
    status: str  # "Registered" or "Pending"
    productModel: str  # Product model name (e.g., "FortiGate-60F")
    productModelEoR: str  # End of Repair date
    productModelEoS: str  # End of Support date
    warrantySupport: str  # Warranty support level
    entitlements: list  # List of entitlements


class LicenseInfo(TypedDict, total=False):
    """License information from FortiCare API."""
    
    serialNumber: str  # Product serial number
    licenseNumber: str  # License number
    registrationCode: str  # License registration code
    description: str  # License description
    startDate: str  # License start date
    endDate: str  # License end date
    status: str  # License status


class ContractInfo(TypedDict, total=False):
    """Contract information from FortiCare API."""
    
    contractNumber: str  # Contract number
    startDate: str  # Contract start date
    endDate: str  # Contract end date
    products: list  # List of products under contract
    status: str  # Contract status


class FolderInfo(TypedDict, total=False):
    """Folder information from FortiCare API."""
    
    folderId: int  # Folder ID
    folderName: str  # Folder name
    folderPath: str  # Full folder path
    parentFolderId: int  # Parent folder ID
    assetCount: int  # Number of assets in folder


__all__ = [
    "AssetInfo",
    "AssetDetailsInfo",
    "LocationInfo",
    "LicenseInfo", 
    "ContractInfo",
    "FolderInfo",
]
