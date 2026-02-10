import cv2
from ultralytics import YOLO

# Use nano model (smallest & fastest)
model = YOLO("yolov8n.pt")

# Reduce camera resolution to lower load
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame further for speed
    small_frame = cv2.resize(frame, (480, 360))

    results = model(small_frame, conf=0.5, device="cpu", verbose=False)

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(small_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    small_frame,
                    "HUMAN",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )

    cv2.imshow("Human Detection (Low System)", small_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
