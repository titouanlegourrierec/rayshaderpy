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

from rayshaderpy.visualization import _plot_map


class TestPlotMap(unittest.TestCase):
    """Test the _plot_map function."""

    def setUp(self):
        """Set up test cases."""
        self.hillshade = np.array([[1, 2], [3, 4]])
        self.output_path = tempfile.NamedTemporaryFile(suffix=".png", delete=True).name

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_valid_input(self):
        """Test when all inputs are valid."""
        try:
            _plot_map(
                hillshade=self.hillshade,
                rotate=90,
                asp=1,
                output_path=self.output_path,
            )
        except Exception as e:
            self.fail(f"_plot_map raised an exception unexpectedly: {e}")

    def test_invalid_hillshade_type(self):
        """Test when hillshade is of an invalid type."""
        with self.assertRaises(ValueError) as context:
            _plot_map(hillshade="invalid", rotate=0)
        self.assertIn("'hillshade' must be of type ndarray", str(context.exception))

    def test_invalid_rotate_value(self):
        """Test when rotate is not a valid value."""
        with self.assertRaises(ValueError) as context:
            _plot_map(hillshade=self.hillshade, rotate=45)
        self.assertIn(
            "'rotate' must be one of [0, 90, 180, 270]",
            str(context.exception),
        )

    def test_invalid_asp_value(self):
        """Test when asp is not a valid value."""
        with self.assertRaises(ValueError) as context:
            _plot_map(hillshade=self.hillshade, rotate=0, asp="invalid")
        self.assertIn("'asp' must be one of ['float', 'int']", str(context.exception))

    def test_output_file_creation(self):
        """Test that the output file is created."""
        _plot_map(hillshade=self.hillshade, output_path=self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    @patch("rpy2.robjects.r")
    @patch("matplotlib.pyplot.imread")
    def test_r_integration(self, mock_imread, mock_r):
        """Test R function integration."""
        mock_r.return_value = None
        mock_imread.return_value = np.array([[1, 2], [3, 4]])  # Mock the image read
        _plot_map(hillshade=self.hillshade, rotate=0, output_path=self.output_path)
        mock_r.assert_called()
        mock_imread.assert_called_with(self.output_path)


if __name__ == "__main__":
    unittest.main()
