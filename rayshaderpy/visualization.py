"""TODO."""

import os
import tempfile
from typing import Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import rpy2.robjects as ro

from .helpers import _assign_variables, _validate_variables


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


def _plot_3d(
    hillshade: np.ndarray,
    heightmap: np.ndarray,
    zscale: float = 1,
    baseshape: str = "rectangle",
    solid: bool = True,
    soliddepth: Union[str, float] = "auto",
    solidcolor: str = "grey20",
    solidlinecolor: str = "grey30",
    shadow: bool = True,
    shadowdepth: Union[str, float] = "auto",
    shadowcolor: str = "auto",
    shadow_darkness: float = 0.5,
    shadowwidth: Union[str, float] = "auto",
    water: bool = False,
    waterdepth: float = 0,
    watercolor: str = "dodgerblue",
    wateralpha: float = 0.5,
    waterlinecolor: Union[str, None] = None,
    waterlinealpha: float = 1,
    linewidth: int = 2,
    lineantialias: bool = False,
    soil: bool = False,
    soil_freq: float = 0.1,
    soil_levels: int = 16,
    soil_color_light: str = "#b39474",
    soil_color_dark: str = "#8a623b",
    soil_gradient: int = 2,
    soil_gradient_darken: int = 4,
    theta: int = 45,
    phi: int = 45,
    fov: int = 0,
    zoom: float = 1,
    background: str = "white",
    windowsize: Union[int, Tuple[int, ...]] = 600,
    precomputed_normals: Union[np.ndarray, None] = None,
    asp: int = 1,
    triangulate: bool = False,
    max_error: float = 0.001,
    max_tri: int = 0,
    verbose: bool = False,
    plot_new: bool = True,
    close_previous: bool = True,
    clear_previous: bool = True,
    output_path: Union[str, None] = None,
) -> None:
    """
    Plot a 3D visualization with the given parameters.

    Parameters:
    ----------
    hillshade : np.ndarray
        Hillshade/image to be added to 3D surface map.
    heightmap : np.ndarray
        A two-dimensional matrix representing elevation. All points are assumed to be evenly spaced.
    zscale : float, default 1
        Ratio between x, y spacing and z axis. For example, if the elevation levels are in units of 1 meter
        and the grid values are separated by 10 meters, 'zscale' would be 10. Adjust the zscale down to
        exaggerate elevation features.
    baseshape : str, default 'rectangle'
        Shape of the base ('rectangle', 'circle', 'hex').
    solid : bool, default True
        If False, only the surface is rendered.
    soliddepth : Union[str, int], default 'auto'
        Depth of the solid base. If heightmap is uniform and set on 'auto', this is automatically set to a
        slightly lower level than the uniform elevation.
    solidcolor : str, default 'grey20'
        Base color.
    solidlinecolor : str, default 'grey30'
        Base edge line color.
    shadow : bool, default True
        If False, no shadow is rendered.
    shadowdepth : Union[str, int], default 'auto'
        Depth of the shadow layer.
    shadowcolor : str, default 'auto'
        Color of the shadow, automatically computed as 'shadow_darkness' the luminance of the 'background'
        color in the CIELuv colorspace if not specified.
    shadow_darkness : float, default 0.5
        Darkness of the shadow, if 'shadowcolor = "auto"'. 0 is no shadow, 1 is black shadow.
    shadowwidth : Union[str, int], default 'auto'
        Width of the shadow in units of the matrix. If 'auto', which sizes it to 1/10th the smallest
        dimension of 'heightmap'.
    water : bool, default False
        If True, a water layer is rendered.
    waterdepth : int, default 0
        Water level.
    watercolor : str, default 'dodgerblue'
        Color of the water.
    wateralpha : float, default 0.5
        Water transparency.
    waterlinecolor : Union[str, None], default None
        Color of the lines around the edges of the water layer.
    waterlinealpha : float, default 1
        Water line tranparency.
    linewidth : int, default 2
        Width of the edge lines in the scene.
    lineantialias : bool, default False
        Whether to anti-alias the lines in the scene.
    soil : bool, default False
        Whether to draw the solid base with a textured soil layer.
    soil_freq : float, default 0.1
        Frequency of soil clumps. Higher frequency values give smaller soil clumps.
    soil_levels : int, default 16
        Fractal level of the soil.
    soil_color_light : str, default '#b39474'
        Light tint of soil.
    soil_color_dark : str, default '#8a623b'
        Dark tint of soil.
    soil_gradient : int, default 2
        Sharpness of the soil darkening gradient. '0' turns off the gradient entirely.
    soil_gradient_darken : int, default 4
        Amount to darken the 'soil_color_dark' value for the deepest soil layers. Higher numbers increase
        the darkening effect.
    theta : int, default 45
        Rotation around z-axis.
    phi : int, default 45
        Azimuth angle.
    fov : int, default 0 (isometric)
        Field-of-view angle.
    zoom : float, default 1
        Zoom factor.
    background : str, default 'white'
        Color of the background.
    windowsize : Union[int, Tuple[int, ...]], default 600
        Position, width, and height of the 'rgl' device displaying the plot. If a single number, viewport
        will be a square and located in upper left corner. If two numbers, (e.g. (600,800)), user will
        specify width and height separately. If four numbers (e.g. (200,0,600,800)), the first two coordinates
        specify the location of the x-y coordinates of the bottom-left corner of the viewport on the screen,
        and the next two (or one, if square) specify the window size. NOTE: The absolute positioning of the
        window does not currently work on macOS, but the size can still be specified.
    precomputed_normals : Union[np.ndarray, None], default None
        Takes the output of 'calculate_normals()' to save computing normals internally.
    asp : int, default 1
        Aspect ratio of the resulting plot. Use 'asp = 1/cospi(mean_latitude/180)' to rescale lat/long at
        higher latitudes to the correct the aspect ratio.
    triangulate : bool, default False
        Reduce the size of the 3D model by triangulating the height map. Set this to True if generating the
        model is slow, or moving it is choppy. Will also reduce the size of 3D models saved to disk.
    max_error : float, default 0.001
        Maximum allowable error when triangulating the height map, when 'triangulate = TRUE'. Increase this
        if you encounter problems with 3D performance, want to decrease render time with 'render_highquality()',
        or need to save a smaller 3D OBJ file to disk with 'save_obj()'.
    max_tri : int, default 0
        Default 0, which turns this setting off and uses 'max_error'. Maximum number of triangles allowed
        with triangulating the height map, when 'triangulate = True'. Increase this if you encounter problems
        with 3D performance, want to decrease render time with 'render_highquality()', or need to save a
        smaller 3D OBJ file to disk with 'save_obj()',
    verbose : bool, default True
        Default True, if 'interactive()'. Prints information about the mesh triangulation if
        'triangulate = TRUE'.
    plot_new : bool, default True
        If True, opens new window with each 'plot_3d()' call. If False, the data will be plotted in the
        same window.
    close_previous : bool, default True
        Closes any previously open 'rgl' window. If False, old windows will be kept open.
    clear_previous : bool, default True
        Clears the previously open 'rgl' window if 'plot_new = FALSE'.
    output_path : Union[str, None], default None
        File path to save the image.
    """

    # fmt: off
    params = {
        "hillshade": (hillshade, np.ndarray), "heightmap": (heightmap, np.ndarray), "zscale": (zscale, (int, float)),
        "baseshape": (baseshape, ["rectangle", "circle", "hex"]), "solid": (solid, bool),
        "soliddepth": (soliddepth, ["auto", float]), "solidcolor": (solidcolor, str), "solidlinecolor": (solidlinecolor, str),
        "shadow": (shadow, bool), "shadowdepth": (shadowdepth, ["auto", float]), "shadowcolor": (shadowcolor, str),
        "shadow_darkness": (shadow_darkness, float), "shadowwidth": (shadowwidth, ["auto", float]), "water": (water, bool),
        "waterdepth": (waterdepth, (float, int)), "watercolor": (watercolor, str), "wateralpha": (wateralpha, float),
        "waterlinecolor": (waterlinecolor, [None, str]), "waterlinealpha": (waterlinealpha, (float, int)),
        "linewidth": (linewidth, int), "lineantialias": (lineantialias, bool), "soil": (soil, bool), "soil_freq": (soil_freq, float),
        "soil_levels": (soil_levels, int), "soil_color_light": (soil_color_light, str), "soil_color_dark": (soil_color_dark, str),
        "soil_gradient": (soil_gradient, int), "soil_gradient_darken": (soil_gradient_darken, int), "theta": (theta, int),
        "phi": (phi, int), "fov": (fov, int), "zoom": (zoom, (float, int)), "background": (background, str),
        "windowsize": (windowsize, (int, tuple)), "precomputed_normals": (precomputed_normals, [None, np.ndarray]),
        "asp": (asp, int), "triangulate": (triangulate, bool), "max_error": (max_error, float), "max_tri": (max_tri, int),
        "verbose": (verbose, bool), "plot_new": (plot_new, bool), "close_previous": (close_previous, bool),
        "clear_previous": (clear_previous, bool), "output_path": (output_path, (str, type(None))),
    }
    # fmt: on

    _validate_variables(params)
    _assign_variables(params)

    if output_path is None:
        path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    else:
        path = output_path
    ro.globalenv["output_path"] = path

    ro.r(
        "rayshader::plot_3d(hillshade=hillshade, heightmap=heightmap, zscale=zscale, baseshape=baseshape, "
        "solid=solid, soliddepth=soliddepth, solidcolor=solidcolor, solidlinecolor=solidlinecolor, shadow=shadow, "
        "shadowdepth=shadowdepth, shadowcolor=shadowcolor, shadow_darkness=shadow_darkness, shadowwidth=shadowwidth, "
        "water=water, waterdepth=waterdepth, watercolor=watercolor, wateralpha=wateralpha, waterlinecolor=waterlinecolor, "
        "waterlinealpha=waterlinealpha, linewidth=linewidth, lineantialias=lineantialias, soil=soil, soil_freq=soil_freq, "
        "soil_levels=soil_levels, soil_color_light=soil_color_light, soil_color_dark=soil_color_dark, soil_gradient=soil_gradient, "
        "soil_gradient_darken=soil_gradient_darken, theta=theta, phi=phi, fov=fov, zoom=zoom, background=background, "
        "windowsize=windowsize, precomputed_normals=precomputed_normals, asp=asp, triangulate=triangulate, max_error=max_error, "
        "max_tri=max_tri, verbose=verbose, plot_new=plot_new, close_previous=close_previous, clear_previous=clear_previous)"
    )
    ro.r("rayshader::render_snapshot(output_path)")

    _display_image(path)

    if output_path is None:
        os.remove(path)


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
