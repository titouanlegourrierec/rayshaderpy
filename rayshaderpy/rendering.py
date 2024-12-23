"""TODO."""

import os
import tempfile
from typing import Any, Optional, Tuple, Union

import rpy2.robjects as ro

from .helpers import _assign_params, _validate_params
from .visualization import _display_image


# Functions for adding features to 3D maps, rendering post-processing effects, and saving snapshots.
def _render_beveled_polygons(self):
    """TODO."""
    # TODO: Implement render_beveled_polygons functionality
    pass


def _render_buildings(self):
    """TODO."""
    # TODO: Implement render_buildings functionality
    pass


def _render_camera(self):
    """TODO."""
    # TODO: Implement render_camera functionality
    pass


def _render_clouds(self):
    """TODO."""
    # TODO: Implement render_clouds functionality
    pass


def _render_compass(self):
    """TODO."""
    # TODO: Implement render_compass functionality
    pass


def _render_contours(self):
    """TODO."""
    # TODO: Implement render_contours functionality
    pass


def _render_depth(self):
    """TODO."""
    # TODO: Implement render_depth functionality
    pass


def _render_floating_overlay(self):
    """TODO."""
    # TODO: Implement render_floating_overlay functionality
    pass


def _render_highquality(
    filename: Optional[str] = None,
    samples: int = 128,
    sample_method: str = "sobol_blue",
    min_variance: float = 1e-07,
    light: bool = True,
    lightdirection: Union[int, Tuple[int, ...]] = 315,
    lightaltitude: Union[int, Tuple[int, ...]] = 45,
    lightsize: Optional[int] = None,
    lightintensity: Union[int, Tuple[int, ...]] = 500,
    lightcolor: Union[str, Tuple[str, ...]] = "white",
    width: Optional[int] = None,
    height: Optional[int] = None,
    line_radius: float = 0.5,
    point_radius: float = 1,
    smooth_line: bool = False,
    use_extruded_paths: bool = False,
    ground_material: Any = None,  # Not yet implemented
    ground_size: int = 100_000,  # Not yet implemented
    scene_elements: Any = None,  # Not yet implemented
    camera_location: Optional[Tuple[float, float, float]] = None,
    camera_lookat: Optional[Tuple[float, float, float]] = None,
    clear: bool = False,
    point_material: Any = None,  # Not yet implemented
    point_material_args: Any = None,  # Not yet implemented
    path_material: Any = None,  # Not yet implemented
    path_material_args: Any = None,  # Not yet implemented
):
    """
    Render a high-quality image of the current scene.

    Parameters
    ----------
    filename : str
        Filename of saved image.
    samples : int, optional
        The maximum number of samples for each pixel. Increase this to increase the quality of the rendering.
    sample_method : str, optional
        Default "sobol_blue", unless 'samples > 256', in which it defaults to "sobol". The type of sampling
        method used to generate random numbers. The other options are "random" (worst quality but fastest),
        "sobol_blue" (best option for sample counts below 256), and "sobol" (slowest but best quality, better
        than `sobol_blue` for sample counts greater than 256).
    min_variance : float, optional
        Default `1e-6`. Minimum acceptable variance for a block of pixels for the adaptive sampler. Smaller
        numbers give higher quality images, at the expense of longer rendering times. If this is set to zero,
        the adaptive sampler will be turned off and the renderer will use the maximum number of samples everywhere.
    light : bool, optional
        Default True. Whether there should be a light in the scene. If not, the scene will be lit with a bluish sky.
    lightdirection : int or Tuple[int, ...], optional
        Default 315. Position of the light angle around the scene. If this is a vector longer than one, multiple
        lights will be generated (using values from 'lightaltitude', 'lightintensity', and 'lightcolor').
    lightaltitude : int or Tuple[int, ...], optional
        Default 45. Angle above the horizon that the light is located. If this is a vector longer than one, multiple
        lights will be generated (using values from 'lightdirection', 'lightintensity', and 'lightcolor')
    lightsize : int, optional
        Default None. Radius of the light(s). Automatically chosen, but can be set here by the user.
    lightintensity : int or Tuple[int, ...], optional
        Default 500. Intensity of the light.
    lightcolor : str or Tuple[str, ...], optional
        Default "white". Color of the light(s).
    width : int, optional
        Defaults to the width of the rgl window. Width of the rendering.
    height : int, optional
        Defaults to the height of the rgl window. Height of the rendering.
    line_radius : float, optional
        Default 0.5. Radius of line/path segments.
    point_radius : float, optional
        Default 1. Radius of 3D points (rendered with 'render_points()' NOTE: not yet implemented). This scales
        the existing value of size specified in 'render_points()'.
    smooth_line : bool, optional
        Default False. If True, the line will be rendered with a continuous smooth line, rather than straight
        segments.
    use_extruded_paths : bool, optional
        Default True. If False, paths will be generated with the 'rayrender::path()' object, instead of
        'rayrender::extruded_path()'.
    ground_material : Any, optional
        Material defined by the rayrender material functions. NOTE: Not yet implemented.
    ground_size : int, optional
        Default 100000. The width of the plane representing the ground.
    scene_elements : Any, optional
        Default None. Extra scene elements to add to the scene, created with rayrender. NOTE: Not yet implemented.
    camera_location : Tuple[float, float, float], optional
        Default None. Custom position of the camera. The `FOV`, `width`, and `height` arguments will still be derived
        from the rgl window.
    camera_lookat : Tuple[float, float, float], optional
        Default None. Custom point at which the camera is directed. The `FOV`, `width`, and `height` arguments will still
        be derived from the rgl window.
    clear : bool, optional
        Default False. If True, the rgl window will be cleared after rendering.
    point_material : Any, optional
        The material to be applied to point data. NOTE: Not yet implemented.
    point_material_args : Any, optional
        The function arguments to 'point_material'. The argument `color` will be automatically extracted from the rgl
        scene, but all other arguments can be specified here. NOTE: Not yet implemented.
    path_material : Any, optional
        The material to be applied to path data. NOTE: Not yet implemented.
    path_material_args : Any, optional
        The function arguments to 'path_material'. The argument `color` will be automatically extracted from the rgl
        scene, but all other arguments can be specified here. NOTE: Not yet implemented.
    """

    # fmt: off
    params = {
        "filename": (filename, (str, type(None))), "samples": (samples, int),
        "sample_method": (sample_method, ["random", "sobol_blue", "sobol"]), "min_variance": (min_variance, (float, int)),
        "light": (light, bool), "lightdirection": (lightdirection, (int, tuple)),
        "lightaltitude": (lightaltitude, (int, tuple)), "lightsize": (lightsize, (int, type(None))),
        "lightintensity": (lightintensity, (int, tuple)), "lightcolor": (lightcolor, (str, tuple)),
        "width": (width, (int, type(None))), "height": (height, (int, type(None))), "line_radius": (line_radius, float),
        "point_radius": (point_radius, (float, int)), "smooth_line": (smooth_line, bool),
        "use_extruded_paths": (use_extruded_paths, bool), "ground_size": (ground_size, int),
        "camera_location": (camera_location, (tuple, type(None))), "camera_lookat": (camera_lookat, (tuple, type(None))),
        "clear": (clear, bool),
    }
    # fmt: on

    _validate_params(params)
    _assign_params(params)

    if filename is None:
        path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    else:
        path = filename
    ro.globalenv["filename"] = path

    ro.r(
        "rayshader::render_highquality(filename=filename, samples=samples, sample_method=sample_method, min_variance=min_variance,"
        "light=light, lightdirection=lightdirection, lightaltitude=lightaltitude, lightsize=lightsize, lightintensity=lightintensity,"
        "lightcolor=lightcolor, width=width, height=height, line_radius=line_radius, point_radius=point_radius,"
        "smooth_line=smooth_line, use_extruded_paths=use_extruded_paths, ground_size=ground_size, camera_location=camera_location,"
        "camera_lookat=camera_lookat, clear=clear)"
    )

    _display_image(path)

    if filename is None:
        os.remove(path)


def _render_label(self):
    """TODO."""
    # TODO: Implement render_label functionality
    pass


def _render_movie(self):
    """TODO."""
    # TODO: Implement render_movie functionality
    pass


def _render_multipolygonz(self):
    """TODO."""
    # TODO: Implement render_multipolygonz functionality
    pass


def _render_obj(self):
    """TODO."""
    # TODO: Implement render_obj functionality
    pass


def _render_path(self):
    """TODO."""
    # TODO: Implement render_path functionality
    pass


def _render_points(self):
    """TODO."""
    # TODO: Implement render_points functionality
    pass


def _render_polygons(self):
    """TODO."""
    # TODO: Implement render_polygons functionality
    pass


def _render_raymesh(self):
    """TODO."""
    # TODO: Implement render_raymesh functionality
    pass


def _render_resize_window(self):
    """TODO."""
    # TODO: Implement render_resize_window functionality
    pass


def _render_scalebar(self):
    """TODO."""
    # TODO: Implement render_scalebar functionality
    pass


def _render_snapshot(self):
    """TODO."""
    # TODO: Implement render_snapshot functionality
    pass


def _render_tree(self):
    """TODO."""
    # TODO: Implement render_tree functionality
    pass


def _render_water(self):
    """TODO."""
    # TODO: Implement render_water functionality
    pass
