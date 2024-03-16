import cv2
import numpy as np
import urllib


class ObjectDetection:
    def __init__(self):
        self.MODEL = cv2.dnn.readNet("models/yolov3.weights", "models/yolov3.cfg")

        self.CLASSES = []
        with open("models/coco.names", "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]

        self.OUTPUT_LAYERS = [
            self.MODEL.getLayerNames()[i - 1]
            for i in self.MODEL.getUnconnectedOutLayers()
        ]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.COLORS /= (np.sum(self.COLORS**2, axis=1) ** 0.5 / 255)[np.newaxis].T

    def detectObj(self, snap):
        height, width, channels = snap.shape
        blob = cv2.dnn.blobFromImage(snap, 1 / 255, (416, 416), swapRB=True, crop=False)

        self.MODEL.setInput(blob)
        outs = self.MODEL.forward(self.OUTPUT_LAYERS)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        data_objects = []

        for i in range(len(boxes)):
            if i in indexes:
                data = {}
                x, y, w, h = boxes[i]
                data["box"] = {"x": x, "y": y, "w": w, "h": h}
                label = str(self.CLASSES[class_ids[i]])

                data["label"] = label
                data_objects.append(data)
        return data_objects

    def LoadImgUrl(self, path):
        url_response = urllib.request.urlopen(path)
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        return cv2.imdecode(img_array, -1)

    def LoadImgFile(self, path):
        return cv2.imread(path)
