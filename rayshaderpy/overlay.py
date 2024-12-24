"""TODO."""

from typing import Optional, Union

import numpy as np
import rpy2.robjects as ro

from .helpers import _assign_params, _validate_params


# Functions for generating overlays to add to maps.
def _generate_altitude_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_altitude_overlay functionality
    pass


def _generate_compass_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_compass_overlay functionality
    pass


def _generate_contour_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_contour_overlay functionality
    pass


def _generate_label_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_label_overlay functionality
    pass


def _generate_line_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_line_overlay functionality
    pass


def _generate_point_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_point_overlay functionality
    pass


def _generate_polygon_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_polygon_overlay functionality
    pass


def _generate_scalebar_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_scalebar_overlay functionality
    pass


def _generate_waterline_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement generate_polygon_overlay functionality
    pass


def _detect_water(
    heightmap: np.ndarray,
    zscale: Union[float, int] = 1,
    cutoff: float = 0.999,
    min_area: Optional[float] = None,
    max_height: Optional[float] = None,
    normalvectors: Optional[np.ndarray] = None,
    keep_groups: bool = False,
    progbar: bool = False,
) -> np.ndarray:
    """
    Detect bodies of water (of a user-defined minimum size) within an elevation matrix.

    Parameters:
    ----------
    heightmap : np.ndarray
        A two-dimensional matrix, where each entry in the matrix is the elevation at that point. All grid
        points are assumed to be evenly spaced. Alternatively, if heightmap is a logical matrix, each
        entry specifies whether that point is water or not.
    zscale : Union[float, int], optional
        Default 1. The ratio between the x and y spacing (which are assumed to be equal) and the z axis.
        For example, if the elevation levels are in units of 1 meter and the grid values are separated by
        10 meters, 'zscale' would be 10.
    cutoff : float, optional
        Default 0.999. The lower limit of the z-component of the unit normal vector to be classified as water.
    min_area : Optional[float], optional
        Minimum area (in units of the height matrix x and y spacing) to be considered a body of water.
        If None, min_area is set to length(heightmap)/400.
    max_height : Optional[float], optional
        Default None. If passed, this number will specify the maximum height a point can be considered to be
        water.
    normalvectors : Optional[np.ndarray], optional
        Default None. Pre-computed array of normal vectors from the 'calculate_normal' function. Supplying
        this will speed up water detection.
    keep_groups : bool, optional
        Default False. If True, the matrix returned will retain the numbered grouping information.

    Returns:
    ----------
    np.ndarray
        Matrix indicating whether water was detected at that point. 1 indicates water, 0 indicates no water.
    """

    if min_area is None:
        min_area = len(heightmap) / 400

    # fmt: off
    params = {"heightmap": (heightmap, np.ndarray), "zscale": (zscale, (float, int)), "cutoff": (cutoff, (float, int)),
              "min_area": (min_area, (float, int)), "max_height": (max_height, Optional[Union[float, int]]),
              "normalvectors": (normalvectors, Optional[np.ndarray]), "keep_groups": (keep_groups, bool),
              "progbar": (progbar, bool),
              }
    # fmt: on

    _validate_params(params)
    _assign_params(params)

    water = ro.r(
        "rayshader::detect_water(heightmap=heightmap, zscale=zscale, cutoff=cutoff, min_area=min_area,"
        "max_height=max_height, normalvectors=normalvectors, keep_groups=keep_groups, progbar=progbar)"
    )

    return water


# Functions adding layers to maps.


def _add_overlay(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement add_overlay functionality
    pass


def _add_shadow(self):  # pragma: no cover
    """TODO."""
    # TODO: Implement add_overlay functionality
    pass


def _add_water(
    hillshade: np.ndarray,  # 3D numpy array representing an RGB image
    watermap: np.ndarray,  # 2D numpy array with values 1 and 0
    color: Optional[str] = "imhof1",
):
    """
    Add a layer of water to a map.

    Parameters:
    ----------
    hillshade : np.ndarray
        A three-dimensional matrix representing an RGB image.
    watermap : np.ndarray
        A two-dimensional matrix with values 1 and 0, where 1 indicates water and 0 indicates no water.
    color : Optional[str], optional
        Default 'imhof1'. The water fill color. A hexcode or recognized color string. Also includes built-in
        colors to match the palettes included in sphere_shade: ('imhof1','imhof2','imhof3','imhof4', 'desert',
        'bw', and 'unicorn').

    Returns:
    ----------
    np.ndarray
        A three-dimensional matrix representing the RGB image with the water layer added.
    """

    # fmt: off
    params = {"hillshade": (hillshade, np.ndarray), "watermap": (watermap, np.ndarray), "color": (color, Optional[str])}
    # fmt: on

    _validate_params(params)

    # Validate hillshade is a 3D numpy array representing an RGB image
    if hillshade.ndim != 3:
        raise ValueError("hillshade must be a 3D numpy array")
    if hillshade.shape[2] != 3:
        raise ValueError("hillshade must have 3 channels representing RGB")

    # Validate watermap is a 2D numpy array with values 1 and 0
    if watermap.ndim != 2:
        raise ValueError("watermap must be a 2D numpy array")
    if not np.all(np.isin(watermap, [0, 1])):
        raise ValueError("watermap must contain only values 1 and 0")

    _assign_params(params)

    hillshade = ro.r(
        "rayshader::add_water(hillshade=hillshade, watermap=watermap, color=color)"
    )

    return hillshade
