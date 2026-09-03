import cv2

RTSP_URL = "rtsp://admin:cmk..n46@192.168.60.220:554/Streaming/Channels/101"

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

print("Kamera açılıyor...")

if not cap.isOpened():
    print("KAMERA AÇILAMADI")
    exit()

print("KAMERA BAĞLANTISI BAŞARILI")

while True:

    ret, frame = cap.read()

    if not ret:
        print("FRAME ALINAMADI")
        continue

    cv2.imshow("Kamera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()