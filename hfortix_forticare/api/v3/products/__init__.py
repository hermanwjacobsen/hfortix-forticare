"""Products API endpoints."""

from .decommission import ProductDecommission
from .description import ProductDescription
from .details import ProductDetails
from .folder import ProductFolder
from .list import ProductList
from .location import ProductLocation
from .register import ProductRegister
from .transfer import ProductTransfer

__all__ = ['ProductDecommission', 'ProductDescription', 'ProductDetails', 'ProductFolder', 'ProductList', 'ProductLocation', 'ProductRegister', 'ProductTransfer']
