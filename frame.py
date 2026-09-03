import cv2
import time
import os

# Kamera bağlantısı
rtsp_url = "rtsp://admin:cmk..n46@192.168.60.220:554/Streaming/Channels/101"
cap = cv2.VideoCapture(rtsp_url)

#
save_dir = "new_images2"
os.makedirs(save_dir, exist_ok=True)


count = 0

existing_files = os.listdir(save_dir)

for filename in existing_files:

    if filename.startswith("frame_") and filename.endswith(".jpg"):

        try:
            number = int(
                filename.replace("frame_", "").replace(".jpg", "")
            )

            if number >= count:
                count = number + 1

        except ValueError:
            pass

print(f"Bir sonraki frame numarası: {count:05d}")


capturing = False
last_capture_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        print("Kameradan görüntü alınamadı.")
        break

    # Görüntü alma aktifse
    if capturing:

        current_time = time.time()

        # Her 1 saniyede bir görüntü al
        if current_time - last_capture_time >= 1:

            filename = os.path.join(
                save_dir,
                f"frame_{count:05d}.jpg"
            )

            cv2.imwrite(filename, frame)

            print(f"Görüntü kaydedildi: {filename}")

            count += 1
            last_capture_time = current_time

    # Ekrana durumu yaz
    status = "AKTIF" if capturing else "DURDU"

    cv2.putText(
        frame,
        f"Goruntu Alma: {status}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if capturing else (0, 0, 255),
        2
    )

    cv2.namedWindow("Bellows Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Bellows Detection", 640, 360)

    cv2.imshow("Bellows Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    # S -> başlat / durdur
    if key == ord("s"):

        capturing = not capturing

        if capturing:
            last_capture_time = time.time()
            print("Görüntü alma BAŞLADI.")
        else:
            print("Görüntü alma DURDU.")

    # Q -> çıkış
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()