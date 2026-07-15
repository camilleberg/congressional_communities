# setting custom colors for the highlight layer
from matplotlib.colors import LinearSegmentedColormap

cc_blue = "#1f3662"
cc_grey = "#f6f9f8"
cc_red = "#b20204"
cc_cream = "#fae8e7"

continuous_colors = [cc_blue, cc_grey, cc_red]
custom_continuous = LinearSegmentedColormap.from_list("my_gradient", continuous_colors)
