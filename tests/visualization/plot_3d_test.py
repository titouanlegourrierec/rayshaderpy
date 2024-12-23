"""Tests for the visualization module."""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib
import numpy as np

matplotlib.use("Agg")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rayshaderpy.visualization import _plot_3d


class TestPlot3D(unittest.TestCase):
    """Test the _plot_3d function."""

    def setUp(self):
        """Set up test cases."""
        self.hillshade = np.array(
            [[0.1, 0.2], [0.3, 0.4]]
        )  # Normalized values between 0 and 1
        self.heightmap = np.array([[10, 20], [30, 40]])
        self.output_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_valid_input(self):
        """Test when all inputs are valid."""
        try:
            _plot_3d(
                hillshade=self.hillshade,
                heightmap=self.heightmap,
                zscale=1,
                output_path=self.output_path,
            )
        except Exception as e:
            self.fail(f"_plot_3d raised an exception unexpectedly: {e}")

    def test_invalid_hillshade_type(self):
        """Test when hillshade is of an invalid type."""
        with self.assertRaises(ValueError) as context:
            _plot_3d(hillshade="invalid", heightmap=self.heightmap, zscale=1)
        self.assertIn(
            "'hillshade' must be of type ndarray, but got str.", str(context.exception)
        )

    def test_invalid_heightmap_type(self):
        """Test when heightmap is of an invalid type."""
        with self.assertRaises(ValueError) as context:
            _plot_3d(hillshade=self.hillshade, heightmap="invalid", zscale=1)
        self.assertIn(
            "'heightmap' must be of type ndarray, but got str.", str(context.exception)
        )

    def test_output_file_creation(self):
        """Test that the output file is created."""
        _plot_3d(
            hillshade=self.hillshade,
            heightmap=self.heightmap,
            zscale=1,
            output_path=self.output_path,
        )
        self.assertTrue(os.path.exists(self.output_path))

    @patch("rpy2.robjects.r")
    @patch("matplotlib.pyplot.imread")
    def test_r_integration(self, mock_imread, mock_r):
        """Test R function integration."""
        mock_r.return_value = None
        mock_imread.return_value = np.array([[1, 2], [3, 4]])  # Mock the image read
        _plot_3d(
            hillshade=self.hillshade,
            heightmap=self.heightmap,
            zscale=1,
            output_path=self.output_path,
        )
        mock_r.assert_called()
        mock_imread.assert_called_with(self.output_path)

    def test_default_parameters(self):
        """Test the function with default parameters."""
        try:
            _plot_3d(hillshade=self.hillshade, heightmap=self.heightmap)
        except Exception as e:
            self.fail(
                f"_plot_3d raised an exception unexpectedly with default parameters: {e}"
            )


if __name__ == "__main__":
    unittest.main()
