"""TODO."""

from .helpers import Helpers
from .overlay import Overlay
from .rendering import Rendering
from .shading import Shading
from .visualization import Visualization


class Renderer:
    """TODO."""

    def __init__(self, dem):
        """TODO."""
        self.helpers = Helpers()
        self.overlay = Overlay()
        self.rendering = Rendering()
        self.shading = Shading()
        self.visualization = Visualization()
