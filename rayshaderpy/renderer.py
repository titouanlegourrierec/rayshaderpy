"""TODO."""

from typing import Optional, Tuple, Union

import numpy as np

from .helpers import _quit, _raster_to_matrix
from .shading import _sphere_shade
from .visualization import _plot_3d, _plot_map


class Renderer:
    """TODO."""

    def __init__(self):
        """Initialize the Renderer class."""
        self.heightmap = None
        self.hillshade = None

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
