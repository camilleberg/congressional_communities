# graph_programs/custom_colors.py
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

cc_blue = "#1f3662"
cc_grey = "#f6f9f8"
cc_red = "#b20204"
cc_cream = "#fae8e7"

# matplotlib
continuous_colors = [cc_blue, cc_red]
_cmap = LinearSegmentedColormap.from_list("my_gradient", continuous_colors)

# converting to plotly 
def matplotlib_to_plotly(cmap, n_colors=255):
    """Convert a matplotlib colormap into a Plotly-compatible colorscale."""
    plotly_colorscale = []
    for i in range(n_colors):
        pos = i / (n_colors - 1)
        r, g, b, _ = cmap(pos)
        plotly_colorscale.append([pos, f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"])
    return plotly_colorscale

custom_continuous = matplotlib_to_plotly(_cmap)