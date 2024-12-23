"""Unit tests for the _r_setup module."""

import os
import subprocess
import sys
import unittest
from unittest.mock import call, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from rayshaderpy._r_setup import install_r_packages


class TestInstallRPackages(unittest.TestCase):
    """Test the install_r_packages method."""

    @patch("rayshaderpy._r_setup.subprocess.run")
    def test_install_r_packages_success(self, mock_run):
        """Test the install_r_packages method with successful calls."""
        # Simulate successful calls for all subprocess.run invocations
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout.decode.return_value = "Success"
        mock_run.return_value.stderr.decode.return_value = ""

        r_library_path = "/fake/path/to/R/library"
        packages_list = ["dplyr", "ggplot2"]

        install_r_packages(r_library_path, packages_list)

        # Expected calls
        expected_calls = [
            call(
                ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call().stdout.decode("utf-8"),
            call(
                ["R", "-e", f'.libPaths("{r_library_path}")'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call().stdout.decode("utf-8"),
            call(
                [
                    "R",
                    "-e",
                    f'install.packages("dplyr", repos="https://cloud.r-project.org", lib="{r_library_path}")',
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call().stdout.decode("utf-8"),
            call(
                [
                    "R",
                    "-e",
                    f'install.packages("ggplot2", repos="https://cloud.r-project.org", lib="{r_library_path}")',
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call().stdout.decode("utf-8"),
        ]

        mock_run.assert_has_calls(expected_calls, any_order=False)

    @patch("rayshaderpy._r_setup.subprocess.run")
    def test_install_r_packages_failure_dir_create(self, mock_run):
        """Test the install_r_packages method with failure in dir.create."""
        # Simulate failure in dir.create
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout.decode.return_value = ""
        mock_run.return_value.stderr.decode.return_value = "Error creating directory"

        r_library_path = "/fake/path/to/R/library"
        packages_list = ["dplyr"]

        with self.assertRaises(SystemExit):
            install_r_packages(r_library_path, packages_list)

        # Validate the correct calls were made
        expected_calls = [
            call(
                ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call().stdout.decode("utf-8"),
            call().stderr.decode("utf-8"),
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)

    @patch("rayshaderpy._r_setup.subprocess.run")
    def test_install_r_packages_failure_libpaths(self, mock_run):
        """Test the install_r_packages method with failure in .libPaths."""
        # Simulate success for dir.create but failure in .libPaths
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["R"], returncode=0, stdout=b"Directory created"
            ),
            subprocess.CompletedProcess(
                args=["R"], returncode=1, stderr=b"Error setting path"
            ),
        ]

        r_library_path = "/fake/path/to/R/library"
        packages_list = ["dplyr"]

        with self.assertRaises(SystemExit):
            install_r_packages(r_library_path, packages_list)

        # Validate the correct calls were made
        expected_calls = [
            call(
                ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call(
                ["R", "-e", f'.libPaths("{r_library_path}")'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)

    @patch("rayshaderpy._r_setup.subprocess.run")
    def test_install_r_packages_failure_install_packages(self, mock_run):
        """Test the install_r_packages method with failure in install.packages."""
        # Simulate success for dir.create and .libPaths, but failure in install.packages
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                args=["R"], returncode=0, stdout=b"Directory created"
            ),  # dir.create success
            subprocess.CompletedProcess(
                args=["R"], returncode=0, stdout=b"Library path set"
            ),  # .libPaths success
            subprocess.CompletedProcess(
                args=["R"], returncode=1, stderr=b"Error installing package"
            ),  # install.packages failure
        ]

        r_library_path = "/fake/path/to/R/library"
        packages_list = ["dplyr"]

        with self.assertRaises(SystemExit):
            install_r_packages(r_library_path, packages_list)

        # Validate the correct calls were made
        expected_calls = [
            call(
                ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call(
                ["R", "-e", f'.libPaths("{r_library_path}")'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            call(
                [
                    "R",
                    "-e",
                    f'install.packages("dplyr", repos="https://cloud.r-project.org", lib="{r_library_path}")',
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)

    @patch("rayshaderpy._r_setup.subprocess.run")
    def test_install_r_packages_file_not_found(self, mock_run):
        """Test the install_r_packages method with FileNotFoundError."""
        # Simulate R not being installed
        mock_run.side_effect = FileNotFoundError()

        r_library_path = "/fake/path/to/R/library"
        packages_list = ["dplyr"]

        with self.assertRaises(SystemExit):
            install_r_packages(r_library_path, packages_list)

        # Validate the correct call was attempted
        expected_calls = [
            call(
                ["R", "-e", f'dir.create("{r_library_path}", showWarnings = FALSE)'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
