"""Tests for the add_water function in overlay.py."""

import os
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rayshaderpy.overlay import _add_water


class TestAddWater(unittest.TestCase):
    """Test the add_water function."""

    def setUp(self):
        """Set up the test data."""
        self.hillshade = np.random.rand(100, 100, 3)  # Valid 3D RGB image
        self.watermap = np.random.choice([0, 1], size=(100, 100))  # Valid 2D watermap

    @patch("rayshaderpy.overlay.ro.r")
    def test_add_water_valid_input(self, mock_r):
        """Test the add_water function with valid input."""
        mock_r.return_value = self.hillshade
        result = _add_water(self.hillshade, self.watermap)
        np.testing.assert_array_equal(result, mock_r.return_value)
        mock_r.assert_called_once()

    def test_add_water_invalid_hillshade_dimension(self):
        """Test the add_water function with invalid hillshade dimensions."""
        hillshade = np.random.rand(100, 100)  # Invalid 2D array
        with self.assertRaises(ValueError, msg="hillshade must be a 3D numpy array"):
            _add_water(hillshade, self.watermap)

    def test_add_water_invalid_hillshade_channels(self):
        """Test the add_water function with invalid hillshade channels."""
        hillshade = np.random.rand(100, 100, 4)  # Invalid number of channels
        with self.assertRaises(
            ValueError, msg="hillshade must have 3 channels representing RGB"
        ):
            _add_water(hillshade, self.watermap)

    def test_add_water_invalid_watermap_dimension(self):
        """Test the add_water function with invalid watermap dimensions."""
        watermap = np.random.rand(100, 100, 2)  # Invalid 3D array
        with self.assertRaises(ValueError, msg="watermap must be a 2D numpy array"):
            _add_water(self.hillshade, watermap)

    def test_add_water_invalid_watermap_values(self):
        """Test the add_water function with invalid watermap values."""
        watermap = np.random.rand(100, 100)  # Invalid values
        with self.assertRaises(
            ValueError, msg="watermap must contain only values 1 and 0"
        ):
            _add_water(self.hillshade, watermap)


if __name__ == "__main__":
    unittest.main()
