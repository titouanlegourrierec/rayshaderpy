"""Helper functions for the rayshaderpy package."""

from typing import Dict, Union

import numpy as np
import rasterio
import rpy2.robjects as ro
from rpy2.robjects import numpy2ri

numpy2ri.activate()


def _assign_params(params: Dict) -> None:
    """
    Assign variables to the R global environment.

    Parameters:
    ----------
    params : dict
        A dictionary of variable names and their values.
    """
    for var_name, (var_value, _) in params.items():
        if isinstance(var_value, type(None)):
            var_value = ro.rinterface.NULL
        elif isinstance(var_value, tuple):
            if all(isinstance(x, (float, int)) for x in var_value):
                var_value = ro.FloatVector(var_value)
            elif all(isinstance(x, str) for x in var_value):
                var_value = ro.StrVector(var_value)
        elif var_name == "normalvectors" and isinstance(var_value, np.ndarray):
            var_value = numpy2ri.py2rpy(var_value)
        ro.globalenv[var_name] = var_value


def _calculate_normal():  # pragma: no cover
    """TODO."""
    # TODO: Implement calculate_normal functionality
    pass


def _quit() -> None:
    """Close the 3D rendering window."""
    ro.r("rgl::close3d()")


def _raster_to_matrix(
    raster: Union[np.ndarray, str],
    interactive: bool = True,
) -> np.ndarray:
    """
    Convert a raster (.tif file) to a numpy.ndarray.

    Parameters:
    ----------
    raster : Union[np.ndarray, str]
        The input raster data as a numpy array or a file path to a .tif file.
    interactive : bool, optional
        If True, prints the dimensions of the matrix.

    Returns:
    ----------
    raster : np.ndarray
        The raster data as a 2D numpy array.

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
                raster = np.flipud(raster)
                raster = np.rot90(raster, k=-1)
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


def _resize_matrix():  # pragma: no cover
    """TODO."""
    # TODO: Implement resize_matrix functionality
    pass


def _validate_params(params: Dict) -> None:
    """
    Validate the input variables.

    Parameters:
    ----------
    params : dict
        A dictionary of variable names and their values.
    """
    for var_name, (var_value, var_type) in params.items():
        if isinstance(var_type, list):
            # Check if var_value is in the list of allowed values
            if var_value not in var_type and not any(
                isinstance(var_value, t) for t in var_type if isinstance(t, type)
            ):
                raise ValueError(
                    f"'{var_name}' must be one of {var_type}, but got {var_value}."
                )
        elif isinstance(var_type, tuple):
            # Check if var_value is an instance of any type in the tuple
            if not any(isinstance(var_value, t) for t in var_type):
                raise ValueError(
                    f"'{var_name}' must be one of {[t.__name__ for t in var_type if hasattr(t, '__name__')]}, but got {type(var_value).__name__}."
                )
        else:
            # Check if var_value is an instance of var_type
            if not isinstance(var_value, var_type):
                raise ValueError(
                    f"'{var_name}' must be of type {var_type.__name__}, but got {type(var_value).__name__}."
                )
