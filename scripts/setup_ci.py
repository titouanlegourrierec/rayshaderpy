"""Setup script for CI."""

import os
import platform
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rayshaderpy.config import PACKAGES_LIST, R_LIBRARY_PATH


def is_r_installed() -> bool:
    """Check if R is installed."""
    try:
        subprocess.run(
            ["R", "--version"],
            check=True,
        )
        return True
    except FileNotFoundError:
        return False


def are_dependencies_installed() -> bool:
    """Check if dependencies for rayshader are installed."""
    try:
        if platform.system() == "Linux":
            subprocess.run(
                ["dpkg", "-s", "gdal-bin", "libgdal-dev", "libproj-dev", "libgeos-dev"],
                check=True,
            )
        return True
    except subprocess.CalledProcessError:
        return False


def install_dependencies():
    """Install dependencies."""
    system = platform.system()

    if system == "Linux":
        try:
            subprocess.run(
                [
                    "sudo",
                    "apt",
                    "install",
                    "gdal-bin",
                    "libgdal-dev",
                    "libproj-dev",
                    "libgeos-dev",
                ],
                check=True,
            )
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing dependencies: {e}")
            sys.exit(1)
    else:
        print("Unsupported operating system.")
        sys.exit(1)


def install_r():
    """Install R."""
    system = platform.system()

    if system == "Linux":
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "r-base"], check=True)
            print("R installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing R: {e}")
            sys.exit(1)
    else:
        print("Unsupported operating system.")
        sys.exit(1)


def install_r_packages():
    """Install rayshader package in R."""
    try:
        r_library_path = R_LIBRARY_PATH

        subprocess.run(
            ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)']
        )
        packages = PACKAGES_LIST
        installed_packages = subprocess.run(
            ["R", "-e", f'installed.packages(lib.loc="{r_library_path}")'],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for package in packages:
            if package not in installed_packages:
                subprocess.run(
                    [
                        "R",
                        "-e",
                        f'install.packages("{package}", repos="https://cloud.r-project.org", lib="{r_library_path}")',
                    ],
                )
            else:
                subprocess.run(
                    [
                        "R",
                        "-e",
                        f'update.packages(oldPkgs="{package}", repos="https://cloud.r-project.org", lib.loc="{r_library_path}", ask=FALSE)',
                    ],
                )
        subprocess.run(
            [
                "R",
                "-e",
                f'installed <- rownames(installed.packages(lib.loc="{r_library_path}")); print(installed)',
            ]
        )

    except FileNotFoundError:
        print("R is not installed.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(
            f"An error occurred while trying to install the R package: {e.stderr or e}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """TODO."""
    if not are_dependencies_installed():
        install_dependencies()
    if not is_r_installed():
        install_r()
    install_r_packages()
