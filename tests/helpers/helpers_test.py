"""TODO."""

import os
import sys
import unittest
from unittest.mock import patch

import numpy as np
import rasterio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
print(sys.path)

from rayshaderpy.helpers import _raster_to_matrix


class TestRasterToMatrix(unittest.TestCase):
    """Test the _raster_to_matrix method."""

    def test_valid_numpy_array(self):
        """Test when input is a valid 2D numpy array."""
        raster = np.array([[1, 2], [3, 4]])
        result = _raster_to_matrix(raster, interactive=False)
        np.testing.assert_array_equal(result, raster)

    def test_invalid_input_type(self):
        """Test when input is neither a numpy array nor a string."""
        with self.assertRaises(ValueError) as context:
            _raster_to_matrix(12345)
        self.assertIn("Input must be a numpy array or a string", str(context.exception))

    def test_invalid_file_extension(self):
        """Test when input file is not a .tif file."""
        with self.assertRaises(ValueError) as context:
            _raster_to_matrix("invalid_file.txt")
        self.assertIn("Input file must be a .tif file", str(context.exception))

    @patch("rasterio.open")
    def test_valid_tif_file(self, mock_rasterio_open):
        """Test when input is a valid .tif file."""
        original_data = np.array([[5, 6], [7, 8]])
        mock_rasterio_open.return_value.__enter__.return_value.read.return_value = (
            original_data
        )

        transformed_data = np.flipud(original_data)
        transformed_data = np.rot90(transformed_data, k=-1)

        result = _raster_to_matrix("valid_file.tif", interactive=False)
        np.testing.assert_array_equal(result, transformed_data)

    def test_file_not_found(self):
        """Test when input file does not exist."""
        with self.assertRaises(FileNotFoundError) as context:
            _raster_to_matrix("non_existent_file.tif")
        self.assertIn("File non_existent_file.tif not found", str(context.exception))

    @patch("rasterio.open")
    def test_invalid_tif_file(self, mock_rasterio_open):
        """Test when input file cannot be read by rasterio."""
        mock_rasterio_open.side_effect = rasterio.errors.RasterioIOError("Read error")
        with self.assertRaises(ValueError) as context:
            _raster_to_matrix("invalid_file.tif")
        self.assertIn("Error reading the file invalid_file.tif", str(context.exception))

    def test_non_2d_numpy_array(self):
        """Test when input numpy array is not 2D."""
        raster = np.array([[[1, 2], [3, 4]]])  # 3D array
        with self.assertRaises(ValueError) as context:
            _raster_to_matrix(raster)
        self.assertIn("Input must be a 2D numpy array", str(context.exception))

    @patch("rasterio.open")
    def test_interactive_output(self, mock_rasterio_open):
        """Test the interactive flag outputs dimensions."""
        mock_data = np.array([[9, 10], [11, 12]])
        mock_rasterio_open.return_value.__enter__.return_value.read.return_value = (
            mock_data
        )

        with patch("builtins.print") as mock_print:
            _raster_to_matrix("valid_file.tif", interactive=True)
            mock_print.assert_called_with("Dimensions of matrix are 2x2")


if __name__ == "__main__":
    unittest.main()
