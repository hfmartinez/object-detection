import cv2
import numpy as np
import base64
from microservices.reports.schemas import Box


class DrawBoxes:
    def __init__(self):
        self.CLASSES = []
        with open("microservices/reports/models/coco.names", "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.COLORS /= (np.sum(self.COLORS**2, axis=1) ** 0.5 / 255)[np.newaxis].T

    def draw_objects(self, img_64, boxes, confidence=None, label=""):
        img = self.load_img_base_64(img_64)
        num_box = 0
        for box in boxes:
            if isinstance(box, dict):
                box = Box(
                    x=box["x"],
                    y=box["y"],
                    w=box["w"],
                    h=box["h"],
                    label=box["label"],
                    confidence=box["confidence"],
                    id=box["id"],
                    owner_id=box["owner_id"],
                )
            if confidence:
                if box.confidence < confidence:
                    continue
            if label:
                if label != box.label:
                    continue
            img = cv2.rectangle(
                img,
                (box.x, box.y),
                (box.x + box.w, box.y + box.h),
                color=self.COLORS[self.CLASSES.index(box.label)],
                thickness=4,
            )
            cv2.putText(
                img,
                box.label,
                (box.x, box.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                self.COLORS[self.CLASSES.index(box.label)],
                2,
            )
            num_box = +1
        base_64_img = self.create_img_base_64(img)
        return base_64_img, num_box

    def create_img_base_64(self, img):
        _, buffer = cv2.imencode(".jpg", img)
        return base64.b64encode(buffer)

    def load_img_base_64(self, img_64):
        nparr = np.fromstring(base64.b64decode(img_64), dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
