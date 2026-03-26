# scripts/visualize_layout.py
import json, cv2
from pathlib import Path

COLORS = {
    "heading"  : (255,   0,   0),
    "paragraph": (  0, 200,   0),
    "list"     : (  0,   0, 255),
    "table"    : (255, 165,   0),
    "code"     : (128,   0, 128),
}

def draw_layout(image_path, layout_json_path):
    img = cv2.imread(str(image_path))
    with open(layout_json_path) as f:
        regions = json.load(f)

    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        label = region["class"]
        color = COLORS.get(label, (200, 200, 200))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    out = f"debug_{Path(image_path).stem}.png"
    cv2.imwrite(out, img)
    print(f"Saved: {out}")
# ADD at the bottom of visualize_layout.py

if __name__ == "__main__":
    results_dir = Path("tests/layout_results")
    
    for json_path in results_dir.glob("*.json"):
        print(f"Processing: {json_path.name}")
        with open(json_path) as f:
            regions = json.load(f)
        if not regions:
            print(f"  Skipping — no regions yet (placeholder)")
            continue
        # draw_layout("path/to/image", json_path)