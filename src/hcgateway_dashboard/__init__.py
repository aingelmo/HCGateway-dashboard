"""HCGateway Dashboard - A Streamlit application for visualizing HCGateway steps data.

This package provides:
- API client for HCGateway authentication and data fetching
- Pydantic models for data validation
- Streamlit-based visualization dashboard
- Comprehensive error handling and logging
"""

__version__ = "0.1.0"
__author__ = "Andres Ingelmo Poveda"
__email__ = "aingelmo@gmail.com"

from hcgateway_dashboard.dashboard import Dashboard
from hcgateway_dashboard.models import StepsData, StepsRecord


__all__ = [
    "Dashboard",
    "StepsData",
    "StepsRecord",
    "__version__",
]
