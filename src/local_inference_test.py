import cv2
from ultralytics import YOLO

# Load the model
model = YOLO('COMEX_bin.pt') 

# Print the dictionary just to verify what ID the Model assigned to PET bottles
print("Model Dictionary:", model.names)

# Camera setup
cap = cv2.VideoCapture(0)
print("COMEX Vision Active... Press 'q' to quit.")


# Main vision loop
while True:
    success, frame = cap.read()
    if not success:
        print("Camera feed lost or blocked! Check Windows Privacy Settings.")
        break

    # Run the model on the current frame at 50% confidence
    results = model(frame, conf=0.5)
    
    # Let YOLO automatically draw the bounding boxes and labels for you
    annotated_frame = results[0].plot()

    # Display the live feed
    cv2.imshow("COMEX Smart Bin - Local PC Test", annotated_frame)

    # Press 'q' to safely shut down the camera
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
