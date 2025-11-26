import cv2

cap = cv2.VideoCapture(0)  # 0 is usually the default camera
if not cap.isOpened():
    print("Error: Could not access the camera.")
else:
    print("Camera initialized successfully.")
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Test Camera", frame)
        else:
            print("Failed to capture image.")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
