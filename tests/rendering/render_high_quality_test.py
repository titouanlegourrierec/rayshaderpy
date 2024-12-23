"""Tests for the render_highquality function."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rayshaderpy.rendering import _render_highquality


class TestRenderHighQuality(unittest.TestCase):
    """Tests for the render_highquality function."""

    @patch("rayshaderpy.rendering._validate_params")
    @patch("rayshaderpy.rendering._assign_params")
    @patch("rayshaderpy.rendering.ro")
    @patch("rayshaderpy.rendering._display_image")
    @patch("os.remove")  # Mock os.remove
    def test_render_highquality_default_params(
        self,
        mock_remove,
        mock_display_image,
        mock_ro,
        mock_assign_params,
        mock_validate_params,
    ):
        """Test the render_highquality function with default parameters."""
        # Mock the R environment and the tempfile
        mock_ro.globalenv = {}
        mock_tempfile = MagicMock()
        mock_tempfile.name = "tempfile.png"
        with patch("tempfile.NamedTemporaryFile", return_value=mock_tempfile):
            _render_highquality()

        # Check if the parameters were validated and assigned
        mock_validate_params.assert_called_once()
        mock_assign_params.assert_called_once()

        # Check if the R function was called with the correct parameters
        mock_ro.r.assert_called_once_with(
            "rayshader::render_highquality(filename=filename, samples=samples, sample_method=sample_method, min_variance=min_variance,"
            "light=light, lightdirection=lightdirection, lightaltitude=lightaltitude, lightsize=lightsize, lightintensity=lightintensity,"
            "lightcolor=lightcolor, width=width, height=height, line_radius=line_radius, point_radius=point_radius,"
            "smooth_line=smooth_line, use_extruded_paths=use_extruded_paths, ground_size=ground_size, camera_location=camera_location,"
            "camera_lookat=camera_lookat, clear=clear)"
        )

        # Check if the image was displayed and the file was removed
        mock_display_image.assert_called_once_with("tempfile.png")
        mock_remove.assert_called_once_with("tempfile.png")

    @patch("rayshaderpy.rendering._validate_params")
    @patch("rayshaderpy.rendering._assign_params")
    @patch("rayshaderpy.rendering.ro")
    @patch("rayshaderpy.rendering._display_image")
    @patch("os.remove")  # Mock os.remove
    def test_render_highquality_with_filename(
        self,
        mock_remove,
        mock_display_image,
        mock_ro,
        mock_assign_params,
        mock_validate_params,
    ):
        """Test the render_highquality function with a specified filename."""
        filename = "test_image.png"
        _render_highquality(filename=filename)

        # Check if the parameters were validated and assigned
        mock_validate_params.assert_called_once()
        mock_assign_params.assert_called_once()

        # Check if the R function was called with the correct parameters
        mock_ro.r.assert_called_once_with(
            "rayshader::render_highquality(filename=filename, samples=samples, sample_method=sample_method, min_variance=min_variance,"
            "light=light, lightdirection=lightdirection, lightaltitude=lightaltitude, lightsize=lightsize, lightintensity=lightintensity,"
            "lightcolor=lightcolor, width=width, height=height, line_radius=line_radius, point_radius=point_radius,"
            "smooth_line=smooth_line, use_extruded_paths=use_extruded_paths, ground_size=ground_size, camera_location=camera_location,"
            "camera_lookat=camera_lookat, clear=clear)"
        )

        # Check if the image was displayed and the file was not removed
        mock_display_image.assert_called_once_with(filename)
        mock_remove.assert_not_called()
