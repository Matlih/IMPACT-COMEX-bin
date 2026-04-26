import cv2
from pathlib import Path
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "COMEX_bin_ncnn_model"

model = YOLO(str(MODEL_PATH), task="detect")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    results = model.predict(frame, verbose=False, imgsz=640, conf=0.1)

    detected_labels = [
        f"{results[0].names[int(cls)]} ({conf:.2f})"
        for cls, conf in zip(results[0].boxes.cls.tolist(), results[0].boxes.conf.tolist())
    ]
    if detected_labels:
        print(f"labels: {', '.join(detected_labels)}")
    else:
        print("labels: none")

    annotated_frame = results[0].plot()
    cv2.imshow("Test", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

    if cv2.getWindowProperty("Test", cv2.WND_PROP_VISIBLE) < 1:
        break