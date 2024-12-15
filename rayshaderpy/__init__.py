"""TODO."""

import logging

from rpy2 import robjects as ro

logger = logging.getLogger(__name__)

from . import _logging  # noqa
from ._r_setup import install_r_packages
from .config import PACKAGES_LIST, R_LIBRARY_PATH


def initialize() -> None:
    """Initialize the R environment by installing required R packages."""
    print(
        "⏳ Initializing the environment. This may take a few minutes at first run... ⏳"
    )
    install_r_packages(R_LIBRARY_PATH, PACKAGES_LIST)
    print(f"Packages installed successfully at: {R_LIBRARY_PATH}")
    print("✅ Environment initialized successfully.")
    print("🚀 You're ready to use rayshaderpy!")


def setup_rayshader():
    """Set up the rayshader environment."""
    try:
        logger.info("Initializing the R environment...")
        ro.r(f".libPaths('{R_LIBRARY_PATH}')")
        ro.r(f"library(rayshader, lib.loc = '{R_LIBRARY_PATH}')")
    except Exception as e:
        if "library(rayshader," in str(e):
            logger.warning("rayshader not found. Installing required packages...")
            try:
                initialize()
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                raise
            ro.r(f"library(rayshader, lib.loc = '{R_LIBRARY_PATH}')")
        else:
            logger.error(f"An error occurred: {e}")
            raise


setup_rayshader()
