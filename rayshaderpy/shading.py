"""TODO."""

from typing import Union

import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import numpy2ri

numpy2ri.activate()


# Functions for generating hillshades.
def _ambient_shade(self):
    """TODO."""
    # TODO: Implement ambient_shade functionality
    pass


def _cloud_shade(self):
    """TODO."""
    # TODO: Implement cloud_shade functionality
    pass


def _constant_shade(self):
    """TODO."""
    # TODO: Implement constant_shade functionality
    pass


def _height_shade(self):
    """TODO."""
    # TODO: Implement height_shade functionality
    pass


def _lamb_shade(self):
    """TODO."""
    # TODO: Implement lamb_shade functionality
    pass


def _ray_shade(self):
    """TODO."""
    # TODO: Implement ray_shade functionality
    pass


def _sphere_shade(
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

    ALLOWED_TEXTURES = [
        "imhof1",
        "imhof2",
        "imhof3",
        "imhof4",
        "desert",
        "bw",
        "unicorn",
    ]

    # Check types of input parameters
    if not isinstance(heightmap, np.ndarray):
        raise ValueError("Heightmap must be a np.ndarray.")
    if heightmap.ndim != 2:
        raise ValueError("Heightmap must be a 2D numpy array.")
    if not isinstance(sunangle, (float, int)):
        raise ValueError("Sunangle must be a float or int.")
    if not isinstance(texture, (np.ndarray, str)):
        raise ValueError("Texture must be a FloatSexpVector, IntSexpVector, or str.")
    elif isinstance(texture, str):
        if texture not in ALLOWED_TEXTURES:
            raise ValueError(f"Texture must be one of {ALLOWED_TEXTURES}.")
    if not isinstance(normalvectors, (np.ndarray, type(None))):
        raise ValueError("Normalvectors must be a numpy array or None.")
    if not isinstance(colorintensity, (float, int)):
        raise ValueError("Colorintensity must be a float or int.")
    if not isinstance(zscale, (float, int)):
        raise ValueError("Zscale must be a float or int.")
    if not isinstance(progbar, bool):
        raise ValueError("Progbar must be a boolean.")

    ro.globalenv["heightmap"] = heightmap
    ro.globalenv["sunangle"] = sunangle
    ro.globalenv["texture"] = texture
    ro.globalenv["normalvectors"] = (
        numpy2ri.py2rpy(normalvectors) if normalvectors is not None else ro.r("NULL")
    )
    ro.globalenv["colorintensity"] = colorintensity
    ro.globalenv["zscale"] = zscale
    ro.globalenv["progbar"] = progbar

    hillshade = ro.r(
        "rayshader::sphere_shade(heightmap, sunangle, texture, normalvectors, colorintensity, zscale, progbar)"
    )
    return hillshade


def _texture_shade(self):
    """TODO."""
    # TODO: Implement texture_shade functionality
    pass


def _create_texture(self):
    """TODO."""
    # TODO: Implement create_texture functionality
    pass
