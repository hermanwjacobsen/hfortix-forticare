"""FortiCare Asset Management V3 API."""

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

    def __init__(self, client: "CloudHTTPClient") -> None:
        """Initialize V3 API with HTTP client."""
        self._client = client

        self.contracts = ContractsCategory(client)
        self.folders = FoldersCategory(client)
        self.licenses = LicensesCategory(client)
        self.products = ProductsCategory(client)
        self.services = ServicesCategory(client)


class ContractsCategory:
    """Contracts endpoints."""

    def __init__(self, client: "CloudHTTPClient") -> None:
        """Initialize category with HTTP client."""
        self.list = contracts.ContractList(client)


class FoldersCategory:
    """Folders endpoints."""

    def __init__(self, client: "CloudHTTPClient") -> None:
        """Initialize category with HTTP client."""
        self.create = folders.FolderCreate(client)
        self.delete = folders.FolderDelete(client)
        self.list = folders.FolderList(client)


class LicensesCategory:
    """Licenses endpoints."""

    def __init__(self, client: "CloudHTTPClient") -> None:
        """Initialize category with HTTP client."""
        self.download = licenses.LicenseDownload(client)
        self.list = licenses.LicenseList(client)
        self.register = licenses.LicenseRegister(client)


class ProductsCategory:
    """Products endpoints."""

    def __init__(self, client: "CloudHTTPClient") -> None:
        """Initialize category with HTTP client."""
        self.decommission = products.ProductDecommission(client)
        self.description = products.ProductDescription(client)
        self.details = products.ProductDetails(client)
        self.folder = products.ProductFolder(client)
        self.list = products.ProductList(client)
        self.location = products.ProductLocation(client)
        self.register = products.ProductRegister(client)
        self.transfer = products.ProductTransfer(client)


class ServicesCategory:
    """Services endpoints."""

    def __init__(self, client: "CloudHTTPClient") -> None:
        """Initialize category with HTTP client."""
        self.register = services.ServiceRegister(client)


__all__ = ['V3API', 'ContractsCategory', 'FoldersCategory', 'LicensesCategory', 'ProductsCategory', 'ServicesCategory']
