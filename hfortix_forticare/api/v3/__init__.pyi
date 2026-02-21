"""Type stubs for FortiCare Asset Management V3 API."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.cloud_client import CloudHTTPClient

from . import contracts
from . import folders
from . import licenses
from . import products
from . import services

class V3API:
    """FortiCare Asset Management V3 API endpoints."""

    contracts: ContractsCategory
    folders: FoldersCategory
    licenses: LicensesCategory
    products: ProductsCategory
    services: ServicesCategory

    def __init__(self, client: CloudHTTPClient) -> None: ...

class ContractsCategory:
    """Contracts endpoints."""

    list: contracts.ContractList

    def __init__(self, client: CloudHTTPClient) -> None: ...

class FoldersCategory:
    """Folders endpoints."""

    create: folders.FolderCreate
    delete: folders.FolderDelete
    list: folders.FolderList

    def __init__(self, client: CloudHTTPClient) -> None: ...

class LicensesCategory:
    """Licenses endpoints."""

    download: licenses.LicenseDownload
    list: licenses.LicenseList
    register: licenses.LicenseRegister

    def __init__(self, client: CloudHTTPClient) -> None: ...

class ProductsCategory:
    """Products endpoints."""

    decommission: products.ProductDecommission
    description: products.ProductDescription
    details: products.ProductDetails
    folder: products.ProductFolder
    list: products.ProductList
    location: products.ProductLocation
    register: products.ProductRegister
    transfer: products.ProductTransfer

    def __init__(self, client: CloudHTTPClient) -> None: ...

class ServicesCategory:
    """Services endpoints."""

    register: services.ServiceRegister

    def __init__(self, client: CloudHTTPClient) -> None: ...

__all__ = ['V3API', 'ContractsCategory', 'FoldersCategory', 'LicensesCategory', 'ProductsCategory', 'ServicesCategory']
