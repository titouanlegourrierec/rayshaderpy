"""Tests for the Shading class."""

import os
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rayshaderpy.shading import _sphere_shade


class TestSphereShade(unittest.TestCase):
    """Test the _sphere_shade method."""

    def test_valid_input(self):
        """Test when all inputs are valid."""
        heightmap = np.array([[1, 2], [3, 4]])
        sunangle = 315
        texture = "imhof1"
        result = _sphere_shade(heightmap=heightmap, sunangle=sunangle, texture=texture)
        self.assertIsInstance(result, np.ndarray)

    def test_invalid_heightmap_type(self):
        """Test when heightmap is of an invalid type."""
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap="invalid", texture="imhof1")
        self.assertIn(
            "'heightmap' must be of type ndarray, but got str.", str(context.exception)
        )

    def test_invalid_heightmap_dimension(self):
        """Test when heightmap is not a 2D numpy array."""
        heightmap = np.array([[[1, 2], [3, 4]]])  # 3D array
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap)
        self.assertIn("Heightmap must be a 2D numpy array.", str(context.exception))

    def test_invalid_sunangle_type(self):
        """Test when sunangle is of an invalid type."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, sunangle="invalid")
        self.assertIn(
            "'sunangle' must be one of ['float', 'int'], but got str.",
            str(context.exception),
        )

    def test_invalid_texture_type(self):
        """Test when texture is of an invalid type."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, texture=12345)
        self.assertIn(
            "'texture' must be one of ['ndarray', 'str'], but got int.",
            str(context.exception),
        )

    def test_invalid_texture_value(self):
        """Test when texture is not in the allowed list."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, texture="invalid_texture")
        self.assertIn("Texture must be one of", str(context.exception))

    def test_invalid_normalvectors_type(self):
        """Test when normalvectors is of an invalid type."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, normalvectors="invalid")
        self.assertIn(
            "'normalvectors' must be one of ['ndarray', 'NoneType'], but got str.",
            str(context.exception),
        )

    def test_invalid_colorintensity_type(self):
        """Test when colorintensity is of an invalid type."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, colorintensity="invalid")
        self.assertIn(
            "'colorintensity' must be one of ['float', 'int'], but got str.",
            str(context.exception),
        )

    def test_invalid_zscale_type(self):
        """Test when zscale is of an invalid type."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, zscale="invalid")
        self.assertIn(
            "'zscale' must be one of ['float', 'int'], but got str.",
            str(context.exception),
        )

    def test_invalid_progbar_type(self):
        """Test when progbar is of an invalid type."""
        heightmap = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError) as context:
            _sphere_shade(heightmap=heightmap, progbar="invalid")
        self.assertIn(
            "'progbar' must be of type bool, but got str.", str(context.exception)
        )

    @patch("rpy2.robjects.r")
    def test_valid_texture_as_numpy_array(self, mock_r):
        """Test when texture is passed as a numpy array."""
        heightmap = np.array([[1, 2], [3, 4]])
        texture = np.array([[0.1, 0.2], [0.3, 0.4]])
        mock_r.return_value = np.array([[0.5, 0.6], [0.7, 0.8]])
        result = _sphere_shade(heightmap=heightmap, texture=texture)
        self.assertIsInstance(result, np.ndarray)
        np.testing.assert_array_equal(result, mock_r.return_value)


if __name__ == "__main__":
    unittest.main()
