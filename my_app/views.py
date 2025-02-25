import torch
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from ultralytics import YOLO
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Load the YOLO model
MODEL_PATH = '/run/media/faisal/DATA/REACT PROJECTS/Test portal final year project/django_backend/myproject/best.pt'
model = YOLO(MODEL_PATH)  # Load the YOLO model using Ultralytics

# Generator function to stream camera frames with object detection
def generate_frames():
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    try:
        while True:
            ret, frame = cap.read()  # Read a frame from the camera
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Perform inference
            results = model(frame)

            # Process results
            current_detections = []
            for result in results:
                if result.boxes is not None:
                    class_indices = result.boxes.cls.cpu().numpy().astype(int)
                    for cls_idx in class_indices:
                        try:
                            object_name = model.names[cls_idx]
                        except IndexError:
                            object_name = f"Unknown Class {cls_idx}"
                        current_detections.append(object_name)

            # Print unique detected objects to console
            unique_detections = list(set(current_detections))
            if unique_detections:
                print("Detected Objects:", ", ".join(unique_detections))

                if "person" in unique_detections and ("copy" in unique_detections or "ear-buds" in unique_detections) :
                        # Send a message to the frontend via WebSocket
                        print("Condition met: Either 'chair' or 'person' is missing.")
                        print(f"Sending WebSocket message: Detected {', '.join(unique_detections)}")
                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(
                            "video_feed_group",  # WebSocket group name
                            {
                                "type": "send_detection_message",
                                "message": f"Detected: {', '.join(unique_detections)}",
                            },
                        )

            # Draw bounding boxes and labels on the frame
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confidences = result.boxes.conf.cpu().numpy()
                    class_ids = result.boxes.cls.cpu().numpy()

                    for box, conf, cls_id in zip(boxes, confidences, class_ids):
                        x1, y1, x2, y2 = box
                        label = model.names[int(cls_id)]
                        confidence = float(conf)

                        # Draw bounding box and label
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, f"{label} {confidence:.2f}", (int(x1), int(y1 - 10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in the response format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Django view to stream camera feed
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")