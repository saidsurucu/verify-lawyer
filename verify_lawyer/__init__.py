"""
Turkish Lawyer Verification Module
Verify and search lawyers in Turkish Bar Association database
"""

from .core import search_lawyers, verify_lawyer

__version__ = "1.0.0"
__all__ = ["search_lawyers", "verify_lawyer"]
