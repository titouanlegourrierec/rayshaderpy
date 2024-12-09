"""TODO."""

from typing import Union

import numpy as np
import rasterio
from rpy2.rinterface import FloatSexpVector, IntSexpVector  # type: ignore
from rpy2.robjects import numpy2ri  # type: ignore

numpy2ri.activate()


class Helpers:
    """TODO."""

    def _calculate_normal(self):
        """TODO."""
        # TODO: Implement calculate_normal functionality
        pass

    def _raster_to_matrix(
        self,
        raster: Union[np.ndarray, str],
        interactive: bool = True,
    ) -> Union[FloatSexpVector, IntSexpVector]:
        """
        Convert a raster (numpy array or .tif file) to an R matrix.

        Parameters:
            - raster (np.ndarray | str): The input raster data as a numpy array or a file path to a .tif file.
            - interactive (bool): If True, prints the dimensions of the matrix.

        Returns:
            - rinterface.FloatSexpVector: The converted R matrix.
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
            except FileNotFoundError:
                raise FileNotFoundError(f"File {raster} not found.")
            except rasterio.errors.RasterioIOError:
                raise ValueError(f"Error reading the file {raster}.")

        # Ensure raster is a 2D numpy array
        if raster.ndim != 2:
            raise ValueError("Input must be a 2D numpy array.")

        # Convert numpy array to R matrix
        matrix = numpy2ri.py2rpy(raster)

        if interactive:
            print(f"Dimensions of matrix are {raster.shape[0]} x {raster.shape[1]}")

        return matrix

    def _resize_matrix(self):
        """TODO."""
        # TODO: Implement resize_matrix functionality
        pass
