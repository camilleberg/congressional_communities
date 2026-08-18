import vgplot as vg

def export_spec(view, output_path):
    with open(output_path, "w") as f:
        f.write(view.to_json(indent=2))   # <-- not json.dump(view, f)
    print(f"Spec written to {output_path}")

if __name__ == "__main__":
    states = vg.spatial("data/us-counties-10m.json", layer="states")
    cc = vg.spatial("data/ccn20_geo_topo.json", layer="data")

    view = vg.plot(
        vg.geo(states, stroke="currentColor", stroke_width=1),
        vg.geo(cc, stroke="currentColor", stroke_width=1, tip=True, title="CCN20"),
        vg.margin(0),
        vg.projection_type("albers"),
    )

    export_spec(view, "map_project/new_map_viz/data/cc_map.spec.json")