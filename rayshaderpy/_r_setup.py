"""Module to install R packages for rayshader."""

import logging
import subprocess
import sys
from typing import List

from tqdm import tqdm

logger = logging.getLogger(__name__)


def install_r_packages(r_library_path: str, PACKAGES_LIST: List[str]):
    """
    Install R packages.

    Parameters
    ----------
        r_library_path (str): Path to the R library.
        PACKAGES_LIST (list): List of R packages to install.
    """
    try:
        result = subprocess.run(
            ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info(f"Creating R library directory: {r_library_path}")
        logger.info(result.stdout.decode("utf-8"))
        if result.returncode != 0:
            logger.error(
                f"Error creating R library directory: {result.stderr.decode('utf-8')}"
            )
            sys.exit(1)
        result = subprocess.run(
            ["R", "-e", f'.libPaths("{r_library_path}")'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info(f"Setting R library path: {r_library_path}")
        logger.info(result.stdout.decode("utf-8"))
        if result.returncode != 0:
            logger.error(
                f"Error setting R library path: {result.stderr.decode('utf-8')}"
            )
            sys.exit(1)
        installed_packages = subprocess.run(
            ["R", "-e", f'installed.packages(lib.loc="{r_library_path}")'],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for package in tqdm(PACKAGES_LIST, desc="Installing R packages"):
            if package not in installed_packages:
                logger.info(f"Installing R package: {package}")
                result = subprocess.run(
                    [
                        "R",
                        "-e",
                        f'install.packages("{package}", repos="https://cloud.r-project.org", lib="{r_library_path}")',
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if result.returncode != 0:
                    logger.error(
                        f"Error installing R package: {result.stderr.decode('utf-8')}"
                    )
                    sys.exit(1)
                else:
                    logger.info(result.stdout.decode("utf-8"))
            else:
                logger.info(f"Updating R package: {package}")
                result = subprocess.run(
                    [
                        "R",
                        "-e",
                        f'update.packages(oldPkgs="{package}", repos="https://cloud.r-project.org", lib.loc="{r_library_path}", ask=FALSE)',
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if result.returncode != 0:
                    logger.error(
                        f"Error updating R package: {result.stderr.decode('utf-8')}"
                    )
                    sys.exit(1)
                else:
                    logger.info(result.stdout.decode("utf-8"))

    except FileNotFoundError:
        logger.critical("R is not installed. Please install R first.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logger.error(
            f"An error occurred while trying to install the R package: {e.stderr or e}"
        )
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        sys.exit(1)
