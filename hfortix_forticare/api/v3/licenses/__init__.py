"""Licenses API endpoints."""

from .download import LicenseDownload
from .list import LicenseList
from .register import LicenseRegister

__all__ = ['LicenseDownload', 'LicenseList', 'LicenseRegister']
