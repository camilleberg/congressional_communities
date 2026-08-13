"""
Convert a dict of GeoJSON-style features into a TopoJSON Topology dict.

Input shape (screenshot 1):
    {
      "1198004": {"DC": "1198", "State": "DC",
                   "geometry": {"type": "Polygon", "coordinates": [...]}},
      ...
    }

Output shape (screenshot 2):
    {
      "type": "Topology",
      "bbox": [...],
      "transform": {"scale": [...], "translate": [...]},
      "objects": {
        "<object_name>": {
          "type": "GeometryCollection",
          "geometries": [
            {"type": "Polygon", "arcs": [...], "id": "...", "properties": {...}},
            ...
          ]
        }
      },
      "arcs": [...]
    }

Requires:  pip install topojson geopandas shapely
"""

import json
import geopandas as gpd
from shapely.geometry import shape
import topojson as tp


def dict_to_topology(
    data: dict,
    object_name: str = "regions",
    id_field: str | None = None,
    property_fields: list[str] | None = None,
    prequantize=1e4,
) -> dict:
    """
    Parameters
    ----------
    data : dict
        Mapping of feature-key -> feature dict. Each feature dict must
        contain a "geometry" key holding a GeoJSON-style geometry
        (type + coordinates). All other keys are treated as attributes.
    object_name : str
        Name to use for the single object inside "objects" (e.g. "counties").
    id_field : str, optional
        Which attribute to use as each geometry's "id". If None, the
        dict's own key is used as the id (matches screenshot 2's
        FIPS-code ids like "04015").
    property_fields : list[str], optional
        Which attributes to keep in "properties". If None, all
        non-geometry, non-id attributes are kept as-is. Pass e.g.
        ["State"] and rename afterwards if you want a "name" key like
        screenshot 2's {"name": "Mohave"}.
    prequantize : int or bool
        Passed straight to topojson.Topology - number of quantization
        bins (produces the delta-encoded "transform" block, matching
        screenshot 2). Set to False to keep full-precision floats and
        drop the "transform" block instead.

    Returns
    -------
    dict : a TopoJSON Topology, ready for json.dumps() / json.dump().
    """
    rows = []
    for key, feature in data.items():
        geom = shape(feature["geometry"])
        attrs = {k: v for k, v in feature.items() if k != "geometry"}

        row_id = attrs.pop(id_field) if id_field else key
        if property_fields is not None:
            attrs = {k: attrs[k] for k in property_fields if k in attrs}

        rows.append({"id": row_id, "geometry": geom, **attrs})

    gdf = gpd.GeoDataFrame(rows, geometry="geometry")
    gdf = gdf.set_index("id", drop=True)

    topo = tp.Topology(gdf, object_name=object_name, prequantize=prequantize)
    return json.loads(topo.to_json())


if __name__ == "__main__":
    # Example: load your dict from a JSON file and convert it.
    #
    # with open("input.json") as f:
    #     data = json.load(f)
    #
    # topology = dict_to_topology(
    #     data,
    #     object_name="counties",
    #     property_fields=["State"],   # -> rename to "name" below if needed
    # )
    #
    # for geom in topology["objects"]["counties"]["geometries"]:
    #     geom["properties"] = {"name": geom["properties"].pop("State")}
    #
    # with open("output_topology.json", "w") as f:
    #     json.dump(topology, f)

    pass