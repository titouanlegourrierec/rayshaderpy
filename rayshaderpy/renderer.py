"""TODO."""

from typing import Union

import numpy as np

from .helpers import _raster_to_matrix
from .shading import _sphere_shade
from .visualization import _plot_map


class Renderer:
    """TODO."""

    def __init__(self):
        """TODO."""
        pass

    def plot_map(
        self,
        hillshade: np.ndarray,
        rotate: int = 0,
        asp: float = 1,
        output_path: Union[str, None] = None,
    ):
        """TODO."""
        return _plot_map(
            hillshade,
            rotate,
            asp,
            output_path,
        )

    def raster_to_matrix(
        self,
        raster: Union[np.ndarray, str],
        interactive: bool = True,
    ) -> np.ndarray:
        """
        Convert a raster (.tif file) to a numpy.ndarray.

        Parameters:
        ----------
            raster (np.ndarray | str): The input raster data as a numpy array or a file path to a .tif file.
            interactive (bool): If True, prints the dimensions of the matrix.

        Returns:
        ----------
            raster (np.ndarray): The raster data as a 2D numpy array.

        Examples:
        ----------
            >>> from rayshaderpy import Renderer
            >>> renderer = Renderer()
            >>> heightmap = renderer.raster_to_matrix("path/to/raster.tif")
        """
        return _raster_to_matrix(raster, interactive)

    def sphere_shade(
        self,
        heightmap: np.ndarray,  # 2D numpy array
        sunangle: Union[float, int] = 315,
        texture: Union[np.ndarray, str] = "imhof1",
        normalvectors: Union[np.ndarray, None] = None,
        colorintensity: Union[float, int] = 1,
        zscale: Union[float, int] = 1,
        progbar: bool = False,
    ) -> np.ndarray:
        """
        Calculate a color for each point on the surface using the surface normals and hemispherical UV mapping.

        This uses either a texture map provided by the user (as an RGB array), or a built-in color texture.

        Parameters
        ----------
        - heightmap (np.ndarray): A two-dimensional matrix, where each entry in the matrix is the elevation
            at that point. All points are assumed to be evenly spaced.
        - sunangle (float | int): Default 315 (NW). The direction of the main highlight color (derived from
            the built-in palettes or the 'create_texture' function).
        - texture (np.ndarray | str): Default 'imhof1'. Either a square matrix indicating the spherical texture
            mapping, or a string indicating one of the built-in palettes ('imhof1','imhof2','imhof3','imhof4',
            'desert', 'bw', and 'unicorn').
        - normalvectors (np.ndarray | None): Default None. Cache of the normal vectors (from 'calculate_normal'
            function). Supply this to speed up texture mapping.
        - colorintensity (float | int): Default 1. The intensity of the color mapping. Higher values will increase
            the intensity of the color mapping.
        - zscale (float | int): Default 1. The ratio between the x and y spacing (which are assumed
            to be equal) and the z axis. Ignored unless 'colorintensity' missing.
        - progbar (bool): Default True if interactive, False otherwise. If False, turns off progress bar.

        Returns
        ----------
        - hillshade (np.ndarray): RGB array of hillshaded texture mappings.
        """
        return _sphere_shade(
            heightmap,
            sunangle,
            texture,
            normalvectors,
            colorintensity,
            zscale,
            progbar,
        )
