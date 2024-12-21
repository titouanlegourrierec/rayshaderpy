"""Configuration file for rayshaderpy package."""

import os
import platform

# Constants for R library paths
_WINDOWS_R_LIBRARY_PATH = "~\\Rlibrary"
_OTHER_R_LIBRARY_PATH = "~/.Rlibrary"

# Determine the R library path based on the operating system
if platform.system() == "Windows":
    R_LIBRARY_PATH = os.path.expanduser(_WINDOWS_R_LIBRARY_PATH)
else:
    R_LIBRARY_PATH = os.path.expanduser(_OTHER_R_LIBRARY_PATH)

# List of required R packages
PACKAGES_LIST = [
    "magick",
    "progress",
    "fs",
    "rappdirs",
    "cachem",
    "memoise",
    "sass",
    "bslib",
    "fontawesome",
    "jquerylib",
    "tinytex",
    "pkgconfig",
    "colorspace",
    "rmarkdown",
    "yaml",
    "fastmap",
    "evaluate",
    "highr",
    "xfun",
    "fansi",
    "utf8",
    "iterators",
    "crayon",
    "hms",
    "prettyunits",
    "R6",
    "sp",
    "terra",
    "cli",
    "farver",
    "glue",
    "labeling",
    "lifecycle",
    "munsell",
    "RColorBrewer",
    "rlang",
    "viridisLite",
    "htmlwidgets",
    "htmltools",
    "knitr",
    "jsonlite",
    "base64enc",
    "mime",
    "tiff",
    "digest",
    "pillar",
    "vctrs",
    "tibble",
    "withr",
    "spacefillr",
    "RcppThread",
    "decido",
    "doParallel",
    "foreach",
    "Rcpp",
    "progress",
    "raster",
    "scales",
    "png",
    "jpeg",
    "magrittr",
    "rgl",
    "terrainmeshr",
    "rayimage",
    "rayvertex",
    "rayrender",
    "RcppArmadillo",
    "rayshader",
    "ambient",  # Optional
]
