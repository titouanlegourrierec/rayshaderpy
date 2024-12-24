"""Tests for the detect_water function."""

import os
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rayshaderpy.overlay import _detect_water


class TestDetectWater(unittest.TestCase):
    """Test the detect_water function."""

    def setUp(self):
        """Set up the test data."""
        self.heightmap = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    @patch("rayshaderpy.overlay.ro.r")
    def test_detect_water_default_params(self, mock_r):
        """Test the detect_water function with default parameters."""
        mock_r.return_value = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        result = _detect_water(self.heightmap)
        np.testing.assert_array_equal(result, mock_r.return_value)
        mock_r.assert_called_once()

    @patch("rayshaderpy.overlay.ro.r")
    def test_detect_water_with_min_area(self, mock_r):
        """Test the detect_water function with min_area parameter."""
        mock_r.return_value = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        result = _detect_water(self.heightmap, min_area=0.5)
        np.testing.assert_array_equal(result, mock_r.return_value)
        mock_r.assert_called_once()

    @patch("rayshaderpy.overlay.ro.r")
    def test_detect_water_with_max_height(self, mock_r):
        """Test the detect_water function with max_height parameter."""
        mock_r.return_value = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        result = _detect_water(self.heightmap, max_height=5)
        np.testing.assert_array_equal(result, mock_r.return_value)
        mock_r.assert_called_once()

    @patch("rayshaderpy.overlay.ro.r")
    def test_detect_water_with_normalvectors(self, mock_r):
        """Test the detect_water function with normalvectors parameter."""
        mock_r.return_value = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        normalvectors = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]])
        result = _detect_water(self.heightmap, normalvectors=normalvectors)
        np.testing.assert_array_equal(result, mock_r.return_value)
        mock_r.assert_called_once()


if __name__ == "__main__":
    unittest.main()
