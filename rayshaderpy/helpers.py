"""Helper functions for the rayshaderpy package."""

from typing import Union

import numpy as np
import rasterio


def _calculate_normal():
    """TODO."""
    # TODO: Implement calculate_normal functionality
    pass


def _raster_to_matrix(
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

    # Check if raster is either a numpy array or a string
    if not isinstance(raster, (np.ndarray, str)):
        raise ValueError(
            "Input must be a numpy array or a string representing a file path."
        )

    # If raster is a string, check if it ends with .tif and read the file
    if isinstance(raster, str):
        if not raster.endswith(".tif"):
            raise ValueError("Input file must be a .tif file.")
        try:
            with rasterio.open(raster) as src:
                raster = np.array(src.read(1))
        except rasterio.errors.RasterioIOError as e:
            if "No such file or directory" in str(e):
                raise FileNotFoundError(f"File {raster} not found.") from e
            else:
                raise ValueError(f"Error reading the file {raster}.") from e

    # Ensure raster is a 2D numpy array
    if raster.ndim != 2:
        raise ValueError("Input must be a 2D numpy array.")

    if interactive:
        print(f"Dimensions of matrix are {raster.shape[0]}x{raster.shape[1]}")

    return raster


def _resize_matrix():
    """TODO."""
    # TODO: Implement resize_matrix functionality
    pass
