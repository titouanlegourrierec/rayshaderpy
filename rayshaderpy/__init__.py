"""TODO."""

from . import _logging  # noqa
from ._r_setup import install_r_packages
from .config import PACKAGES_LIST, R_LIBRARY_PATH


def initialize() -> None:
    """Initialize the R environment by installing required R packages."""
    print("⏳ Initializing the R environment. This may take a few minutes... ⏳")
    install_r_packages(R_LIBRARY_PATH, PACKAGES_LIST)
    print(f"Packages installed successfully at: {R_LIBRARY_PATH}")
    print("✅ Environment initialized successfully.")
    print("🚀 You're ready to use rayshaderpy!")
