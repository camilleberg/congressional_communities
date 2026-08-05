Basically need map extenison to echarts
+ https://github.com/gnijuohz/echarts-leaflet
+ https://echarts.apache.org/en/download-extension.html

**Option B — Use ipyleaflet for the map, and feed pyecharts data from clicks/interactions**  
If your goal is "click a region on the map → show a pyecharts chart for that region," you'd wire up an ipyleaflet event handler (`on_click`, `on_hover`) that re-renders a pyecharts chart into an `Output` widget:
+ https://ywu120766.medium.com/ipyleaflet-ipywidgets-interactive-map-in-jupyter-notebook-a6ba76586cb5