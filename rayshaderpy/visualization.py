"""TODO."""

import os
import tempfile
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import rpy2.robjects as ro


# Functions for displaying/saving 2D visualizations and 3D prints/models
def _display_image(image_path: str) -> None:
    """
    Display the image using matplotlib.

    Parameters:
        - image_path (str): The file path to the image to be displayed.

    Returns:
        - None
    """
    img = plt.imread(image_path)
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis("off")
    plt.show()


def _plot_3d(self):
    """TODO."""
    # TODO: Implement plot_3d functionality
    pass


def _plot_gg(self):
    """TODO."""
    # TODO: Implement plot_gg functionality
    pass


def _plot_map(
    hillshade: np.ndarray,
    rotate: int = 0,
    asp: float = 1,
    output_path: Union[str, None] = None,
) -> None:
    """
    Plot a map with the given parameters.

    Parameters:
    ----------
        - hillshade (np.ndarray or None): Hillshade to be plotted.
        - rotate (int): Default 0. Rotates the output. Possible values: 0, 90, 180, 270.
        - asp (float or int): Default 1. Aspect ratio of the resulting plot. Use
    asp = 1/cospi(mean_latitude/180) to rescale lat/long at higher latitudes to the correct
    the aspect ratio.
        - output_path (str): Default None. File path to save the image.

    Returns:
    ----------
        - None
    """

    # Check types of input parameters
    if not isinstance(hillshade, (np.ndarray)):
        raise ValueError("hillshade must be a np.ndarray, or None.")
    if rotate not in [0, 90, 180, 270]:
        raise ValueError("rotate must be one of the following values: 0, 90, 180, 270.")
    if not isinstance(asp, (float, int)):
        raise ValueError("asp must be a float or int.")

    if not isinstance(output_path, (str, type(None))):
        raise ValueError("filepath must be a string or None.")

    ro.globalenv["hillshade"] = hillshade
    ro.globalenv["rotate"] = rotate
    ro.globalenv["asp"] = asp

    if output_path is None:
        path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    else:
        path = output_path
    ro.r(f'png("{path}")')
    ro.r("rayshader::plot_map(hillshade=hillshade, rotate=rotate, asp=asp)")
    ro.r("dev.off()")

    _display_image(path)

    if output_path is None:
        os.remove(path)


def _save_3dprint(self):
    """TODO."""
    # TODO: Implement save_3dprint functionality
    pass


def _save_multipolygonz_to_obj(self):
    """TODO."""
    # TODO: Implement save_multipolygonz_to_obj functionality
    pass


def _save_obj(self):
    """TODO."""
    # TODO: Implement save_obj functionality
    pass


def _save_png(self):
    """TODO."""
    # TODO: Implement save_png functionality
    pass


def _convert_path_to_animation_coords(self):
    """TODO."""
    # TODO: Implement convert_path_to_animation_coords functionality
    pass


def _convert_rgl_to_raymesh(self):
    """TODO."""
    # TODO: Implement convert_rgl_to_raymesh functionality
    pass
