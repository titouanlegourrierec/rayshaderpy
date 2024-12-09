"""TODO."""

import os
import sys
from unittest.mock import patch

import numpy as np
import pytest
import rasterio
import rpy2  # type: ignore
from rpy2.robjects import numpy2ri  # type: ignore

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rayshaderpy.helpers import Helpers

numpy2ri.activate()


class TestRasterToMatrix:
    """Class to test the _raster_to_matrix method of the Helpers class."""

    def setup_method(self):
        """Create an instance of the Helpers class for each test."""
        self.helpers = Helpers()

    def test_numpy_array_input(self):
        """Test that the method returns a R matrix when given a numpy array."""
        raster = np.array([[1, 2], [3, 4]])
        result = self.helpers._raster_to_matrix(raster)

        assert isinstance(
            result, (rpy2.rinterface.IntSexpVector, rpy2.rinterface.FloatSexpVector)
        )

        numpy_result = numpy2ri.rpy2py(result)

        assert numpy_result.shape == (2, 2)
        assert np.array_equal(numpy_result, raster)

    def test_tif_file_input(self):
        """Test that the method returns a R matrix when given a .tif file."""
        mock_raster_data = np.array([[5, 6], [7, 8]])

        with patch("rasterio.open") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                mock_raster_data
            )

            result = self.helpers._raster_to_matrix("mock_file.tif")

            assert isinstance(
                result, (rpy2.rinterface.IntSexpVector, rpy2.rinterface.FloatSexpVector)
            )

    def test_invalid_input_type(self):
        """Test that the method raises a ValueError when given an invalid input type."""
        with pytest.raises(
            ValueError,
            match="Input must be a numpy array or a string representing a file path.",
        ):
            self.helpers._raster_to_matrix(123)

    def test_invalid_tif_extension(self):
        """Test that the method raises a ValueError when given a file with an invalid extension."""
        with pytest.raises(ValueError, match="Input file must be a .tif file."):
            self.helpers._raster_to_matrix("invalid_file.txt")

    def test_file_not_found(self):
        """Test that the method raises a FileNotFoundError when the file is not found."""
        with patch("rasterio.open", side_effect=FileNotFoundError):
            with pytest.raises(
                FileNotFoundError, match="File mock_file.tif not found."
            ):
                self.helpers._raster_to_matrix("mock_file.tif")

    def test_rasterio_io_error(self):
        """Test that the method raises a ValueError when rasterio encounters an error."""
        with patch("rasterio.open", side_effect=rasterio.errors.RasterioIOError):
            with pytest.raises(
                ValueError, match="Error reading the file mock_file.tif."
            ):
                self.helpers._raster_to_matrix("mock_file.tif")

    def test_non_2d_array(self):
        """Test that the method raises a ValueError when given a non-2D numpy array."""
        invalid_raster = np.array([[[1, 2], [3, 4]]])  # 3D array
        with pytest.raises(ValueError, match="Input must be a 2D numpy array."):
            self.helpers._raster_to_matrix(invalid_raster)

    def test_interactive_flag(self, capsys):
        """Test that the method prints the dimensions of the matrix when interactive=True."""
        raster = np.array([[1, 2], [3, 4]])
        self.helpers._raster_to_matrix(raster, interactive=True)

        captured = capsys.readouterr()
        assert "Dimensions of matrix are 2 x 2" in captured.out
