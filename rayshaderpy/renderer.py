"""TODO."""

from typing import Any, Optional, Tuple, Union

import numpy as np

from .helpers import _quit, _raster_to_matrix
from .overlay import _add_water, _detect_water
from .rendering import _render_highquality
from .shading import _sphere_shade
from .visualization import _plot_3d, _plot_map


class Renderer:
    """TODO."""

    def __init__(self):
        """Initialize the Renderer class."""
        self.heightmap = None
        self.hillshade = None
        self.watermap = None

    def add_water(
        self,
        hillshade: Optional[np.ndarray] = None,  # 3D numpy array of an RGB image
        watermap: Optional[np.ndarray] = None,  # 2D numpy array with values 1 and 0
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
        if hillshade is None:
            if self.hillshade is None:
                raise ValueError("hillshade is missing.")
            hillshade = self.hillshade
        if watermap is None:
            if self.watermap is None:
                raise ValueError("watermap is missing.")
            watermap = self.watermap
        params = locals()
        del params["self"]
        self.hillshade = _add_water(**params)
        return self.hillshade

    def detect_water(
        self,
        heightmap: Optional[np.ndarray] = None,
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
        if heightmap is None:
            if self.heightmap is None:
                raise ValueError("heightmap is missing.")
            heightmap = self.heightmap
        params = locals()
        del params["self"]
        self.watermap = _detect_water(**params)
        return self.watermap

    def plot_3d(
        self,
        hillshade: Optional[np.ndarray] = None,
        heightmap: Optional[np.ndarray] = None,
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
        waterlinecolor: Optional[str] = None,
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
        zoom: int = 1,
        background: str = "white",
        windowsize: Union[int, Tuple[int, ...]] = 600,
        precomputed_normals: Optional[np.ndarray] = None,
        asp: int = 1,
        triangulate: bool = False,
        max_error: float = 0.001,
        max_tri: int = 0,
        verbose: bool = False,
        plot_new: bool = True,
        close_previous: bool = True,
        clear_previous: bool = True,
        output_path: Optional[str] = None,
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
        if heightmap is None:
            if self.heightmap is None:
                raise ValueError("heightmap is missing.")
            heightmap = self.heightmap
        if hillshade is None:
            if self.hillshade is None:
                raise ValueError("hillshade is missing.")
            hillshade = self.hillshade
        params = locals()
        del params["self"]
        return _plot_3d(**params)

    def plot_map(
        self,
        hillshade: Optional[np.ndarray] = None,
        rotate: int = 0,
        asp: float = 1,
        output_path: Optional[str] = None,
    ):
        """
        Plot a map with the given parameters.

        Parameters:
        ----------
        hillshade : np.ndarray
            Hillshade to be plotted.
        rotate : int
            Default 0. Rotates the output. Possible values: 0, 90, 180, 270.
        asp : float
            Default 1. Aspect ratio of the resulting plot. Use asp = 1/cospi(mean_latitude/180) to rescale lat/long
            at higher latitudes to the correct the aspect ratio.
        output_path : Union[str, None]
            Default None. File path to save the image.

        Returns:
        ----------
            None
        """
        if hillshade is None:
            if self.hillshade is None:
                raise ValueError("hillshade is missing.")
            hillshade = self.hillshade
        params = locals()
        del params["self"]
        return _plot_map(**params)

    def quit(self):
        """Close the 3D rendering window."""
        return _quit()

    def raster_to_matrix(
        self,
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
        params = locals()
        del params["self"]
        self.heightmap = _raster_to_matrix(**params)
        return self.heightmap

    def render_highquality(
        self,
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
        params = locals()
        del params["self"]
        return _render_highquality(**params)

    def sphere_shade(
        self,
        heightmap: Optional[np.ndarray] = None,  # 2D numpy array
        sunangle: Union[float, int] = 315,
        texture: Union[np.ndarray, str] = "imhof1",
        normalvectors: Optional[np.ndarray] = None,
        colorintensity: Union[float, int] = 1,
        zscale: Union[float, int] = 1,
        progbar: bool = False,
    ) -> np.ndarray:
        """
        Calculate a color for each point on the surface using the surface normals and hemispherical UV mapping.

        This uses either a texture map provided by the user (as an RGB array), or a built-in color texture.

        Parameters
        ----------
        heightmap : np.ndarray
            A two-dimensional matrix, where each entry in the matrix is the elevation at that point. All points
            are assumed to be evenly spaced.
        sunangle : Union[float, int], optional
            Default 315 (NW). The direction of the main highlight color (derived from the built-in palettes or
            the 'create_texture' function).
        texture : Union[np.ndarray, str], optional
            Default 'imhof1'. Either a square matrix indicating the spherical texture mapping, or a string indicating
            one of the built-in palettes ('imhof1','imhof2','imhof3','imhof4', 'desert', 'bw', and 'unicorn').
        normalvectors : Union[np.ndarray, None], optional
            Default None. Cache of the normal vectors (from 'calculate_normal' function). Supply this to speed up
            texture mapping.
        colorintensity : Union[float, int], optional
            Default 1. The intensity of the color mapping. Higher values will increase the intensity of the color mapping.
        zscale : Union[float, int], optional
            Default 1. The ratio between the x and y spacing (which are assumed to be equal) and the z axis. Ignored
            unless 'colorintensity' missing.
        progbar : bool, optional
            Default True if interactive, False otherwise. If False, turns off progress bar.

        Returns
        ----------
        np.ndarray
            A 2D numpy array representing the hillshade.
        """
        if heightmap is None:
            if self.heightmap is None:
                raise ValueError("heightmap is missing.")
            heightmap = self.heightmap
        params = locals()
        del params["self"]
        self.hillshade = _sphere_shade(**params)
        return self.hillshade
