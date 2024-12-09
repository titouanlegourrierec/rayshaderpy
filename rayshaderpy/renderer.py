"""TODO."""

from typing import Union

import numpy as np
from rpy2.rinterface import FloatSexpVector, IntSexpVector  # type: ignore

from .helpers import Helpers
from .overlay import Overlay
from .rendering import Rendering
from .shading import Shading
from .visualization import Visualization


class Renderer:
    """TODO."""

    def __init__(self):
        """TODO."""
        self.helpers = Helpers()
        self.overlay = Overlay()
        self.rendering = Rendering()
        self.shading = Shading()
        self.visualization = Visualization()

    def raster_to_matrix(
        self,
        raster: Union[np.ndarray, str],
        interactive: bool = True,
    ) -> Union[FloatSexpVector, IntSexpVector]:
        """Convert a raster (numpy array or .tif file) to an R matrix."""
        return self.helpers._raster_to_matrix(raster, interactive)
