import xml.etree.ElementTree as ET
import os
import copy

# Load original SVG
svg_path = "393390-PCQI1Y-158.svg"
output_dir = "tracks_svg"
os.makedirs(output_dir, exist_ok=True)

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_path)
root = tree.getroot()

# Get viewBox and width/height
viewBox = root.attrib.get("viewBox")
width = root.attrib.get("width")
height = root.attrib.get("height")

# Find all <path> elements (skip the border/background path, usually the first)
paths = [p for p in root.iter() if p.tag.endswith('path')]

for i, path in enumerate(paths):
    # Optionally skip first path if it's a background/border
    if i == 0 and "H" in path.attrib.get("d", ""):
        continue

    # Make a copy of the path so we don't mess with the original tree
    path_copy = copy.deepcopy(path)

    # Create new SVG root with only the copied path
    track_svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
    })
    if viewBox: track_svg.set("viewBox", viewBox)
    if width: track_svg.set("width", width)
    if height: track_svg.set("height", height)
    track_svg.append(path_copy)

    track_tree = ET.ElementTree(track_svg)
    track_id = path.attrib.get("id", f"track{i+1}")
    out_path = os.path.join(output_dir, f"{track_id}.svg")
    track_tree.write(out_path, encoding="utf-8", xml_declaration=True)

print(f"Extracted {len(paths)-1} track SVGs into '{output_dir}' folder.")
