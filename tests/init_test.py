"""Tests for the initialization functions."""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rayshaderpy import R_LIBRARY_PATH, initialize, setup_rayshader


class TestInitialize(unittest.TestCase):
    """Test the initialize function."""

    @patch("rayshaderpy.install_r_packages")
    @patch("builtins.print")
    def test_initialize_success(self, mock_print, mock_install_r_packages):
        """Test if initialize() works correctly."""
        # Test if initialize() works correctly
        mock_install_r_packages.return_value = None
        initialize()
        mock_install_r_packages.assert_called_once_with(
            R_LIBRARY_PATH, unittest.mock.ANY
        )
        mock_print.assert_any_call(
            "⏳ Initializing the environment. This may take a few minutes at first run... ⏳"
        )
        mock_print.assert_any_call(
            f"Packages installed successfully at: {R_LIBRARY_PATH}"
        )
        mock_print.assert_any_call("✅ Environment initialized successfully.")
        mock_print.assert_any_call("🚀 You're ready to use rayshaderpy!")

    @patch("rayshaderpy.install_r_packages", side_effect=Exception("Install error"))
    @patch("builtins.print")
    def test_initialize_failure(self, mock_print, mock_install_r_packages):
        """Test if initialize() handles an error correctly."""
        # Test if initialize() handles an error correctly
        with self.assertRaises(Exception) as context:
            initialize()
        self.assertEqual(str(context.exception), "Install error")


class TestSetupRayshader(unittest.TestCase):
    """Test the setup_rayshader function."""

    @patch("rayshaderpy.ro.r")
    @patch("rayshaderpy.initialize")
    @patch("rayshaderpy.logger")
    def test_setup_rayshader_success(self, mock_logger, mock_initialize, mock_r):
        """Test if setup_rayshader() works correctly."""
        # Test if setup_rayshader() works correctly
        mock_r.return_value = None
        setup_rayshader()
        mock_r.assert_any_call(f".libPaths('{R_LIBRARY_PATH}')")
        mock_r.assert_any_call(f"library(rayshader, lib.loc = '{R_LIBRARY_PATH}')")
        mock_logger.info.assert_called_with("Initializing the R environment...")
        mock_initialize.assert_not_called()

    @patch(
        "rayshaderpy.ro.r",
        side_effect=[Exception("library(rayshader, not found"), None],
    )
    @patch("rayshaderpy.initialize")
    @patch("rayshaderpy.logger")
    def test_setup_rayshader_install_and_retry(
        self, mock_logger, mock_initialize, mock_r
    ):
        """Test if setup_rayshader() installs missing packages and retries."""
        # Test if setup_rayshader() installs missing packages and retries
        mock_initialize.return_value = None
        setup_rayshader()
        mock_initialize.assert_called_once()
        mock_logger.warning.assert_called_with(
            "rayshader not found. Installing required packages..."
        )
        mock_r.assert_any_call(f"library(rayshader, lib.loc = '{R_LIBRARY_PATH}')")

    @patch("rayshaderpy.ro.r", side_effect=Exception("Unexpected error"))
    @patch("rayshaderpy.logger")
    def test_setup_rayshader_unexpected_error(self, mock_logger, mock_r):
        """Test if setup_rayshader() raises an unexpected exception."""
        # Test if setup_rayshader() raises an unexpected exception
        with self.assertRaises(Exception) as context:
            setup_rayshader()
        self.assertEqual(str(context.exception), "Unexpected error")
        mock_logger.error.assert_called_with("An error occurred: Unexpected error")
