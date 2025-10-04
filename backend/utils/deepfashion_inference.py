import cv2
import numpy as np
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo

def load_deepfashion_model(weights_path):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 13  # DeepFashion2 categories
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = weights_path
    cfg.MODEL.DEVICE = "cpu"  # CPU-only
    return DefaultPredictor(cfg)

def run_deepfashion_inference(image_path, predictor):
    """Detect garments and return bounding boxes + category names."""
    image = cv2.imread(image_path)
    outputs = predictor(image)
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()
    classes = instances.pred_classes.numpy()

    category_map = {
        0: "short sleeve top", 1: "long sleeve top", 2: "short sleeve outwear",
        3: "long sleeve outwear", 4: "vest", 5: "sling", 6: "shorts",
        7: "trousers", 8: "skirt", 9: "short sleeve dress",
        10: "long sleeve dress", 11: "vest dress", 12: "sling dress"
    }

    results = []
    for box, cls_id in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box)
        category = category_map.get(cls_id, "unknown")
        results.append({
            "bounding_box": [x1, y1, x2, y2],
            "category": category
        })
    return results