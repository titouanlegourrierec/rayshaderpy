"""TODO."""

from typing import Union

import numpy as np

from .helpers import _raster_to_matrix


class Renderer:
    """TODO."""

    def __init__(self):
        """TODO."""
        pass

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
