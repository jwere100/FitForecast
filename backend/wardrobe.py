from pathlib import Path
from datetime import datetime
from PIL import Image
import cv2
import numpy as np
from utils.deepfashion_inference import load_deepfashion_model, run_deepfashion_inference
from scipy.spatial import KDTree

# ----------------------------
# Load Detectron2 model globally
# ----------------------------
predictor = load_deepfashion_model(
    weights_path="backend/models/deepfashion2_mask_rcnn_R_50_FPN_3x.pth"
)

# ----------------------------
# Build 500+ color palette

COLOR_PALETTE = {}
step = 32  # RGB step to generate ~512 colors
i = 0
for r in range(0, 256, step):
    for g in range(0, 256, step):
        for b in range(0, 256, step):
            COLOR_PALETTE[f"color_{i}"] = (r, g, b)
            i += 1

palette_lab = []
color_names = []
for name, rgb in COLOR_PALETTE.items():
    bgr = np.uint8([[rgb[::-1]]])  # RGB -> BGR
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[0][0]
    palette_lab.append(lab)
    color_names.append(name)

color_tree = KDTree(palette_lab)

# ----------------------------
# Utility functions
# ----------------------------
async def save_uploaded_image(file, upload_dir="uploads"):
    """Save uploaded file asynchronously and return its path."""
    upload_path = Path(upload_dir)
    upload_path.mkdir(exist_ok=True)
    file_path = upload_path / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return str(file_path)


def crop_background(image_path, detections):
    """Crop non-clothing areas based on bounding boxes."""
    image = cv2.imread(image_path)
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    for det in detections:
        x1, y1, x2, y2 = det["bounding_box"]
        mask[y1:y2, x1:x2] = 255

    result = cv2.bitwise_and(image, image, mask=mask)
    cropped_path = str(Path(image_path).with_name(f"cropped_{Path(image_path).name}"))
    cv2.imwrite(cropped_path, result)
    return cropped_path


def classify_color(avg_bgr):
    """Classify average color to nearest in 500+ palette using Lab space."""
    b, g, r = avg_bgr
    bgr = np.uint8([[[b, g, r]]])
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[0][0]
    _, idx = color_tree.query(lab)
    return color_names[idx]


def extract_color_pattern(image_path, bbox):
    """Estimate dominant color in the bounding box (pattern placeholder)."""
    x1, y1, x2, y2 = bbox
    image = cv2.imread(image_path)[y1:y2, x1:x2]
    avg_color = image.mean(axis=(0, 1))  # BGR average
    color_name = classify_color(avg_color)
    pattern_name = "unknown"  # Can enhance later with ML
    return color_name, pattern_name


def extract_attributes(image_path, uploaded_by="user123"):
    """Detect garments, crop background, and return metadata with 500+ color support."""
    detections = run_deepfashion_inference(image_path, predictor)
    cropped_path = crop_background(image_path, detections)

    metadata_items = []
    for det in detections:
        color, pattern = extract_color_pattern(image_path, det["bounding_box"])
        item_metadata = {
            "filename": Path(cropped_path).name,
            "name": "Unknown Name",
            "type": det["category"],
            "brand": "Unknown",
            "color": color,
            "pattern": pattern,
            "material": "Unknown",
            "size": "M",
            "fit": "regular",
            "season": ["spring", "summer"],
            "occasion": ["casual"],
            "style_tags": [],
            "uploaded_by": uploaded_by,
            "date_added": datetime.now().strftime("%Y-%m-%d"),
            "version": 1,
            "times_worn": 0,
            "compatible_items": []
        }
        metadata_items.append(item_metadata)

    return {"metadata": metadata_items, "cropped_image": cropped_path}