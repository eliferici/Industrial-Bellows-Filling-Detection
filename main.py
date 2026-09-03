from ultralytics import YOLO
import cv2
consecutive_filling_frames = 0
REQUIRED_FRAMES = 5
RTSP_URL = "..."


model = YOLO(r"C:\Users\erici\Downloads\lexigrid\lexigrid\docs\detection\runs\detect\train\weights\best.pt")
class_names = {
    1: "Körük",
    2: "Cover Open",
}




cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("Kamera açılamadı.")
    exit()

print("Kamera bağlantısı başarılı.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Kameradan görüntü alınamadı.")
        break


    results = model(frame, verbose=False)
    results[0].names = class_names

    filling_status = "DOLUM GERÇEKLEŞMİYOR"

    frame_height, frame_width = frame.shape[:2]


    annotated_frame = results[0].plot().copy()

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        if class_id == 1:

         
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            cv2.circle(
                annotated_frame,
                (center_x, center_y),
                7,
                (255, 0, 0),
                -1
            )

            cv2.putText(
                annotated_frame,
                f"Center: ({center_x}, {center_y})",
                (center_x + 10, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )


            cv2.line(
                annotated_frame,
                (center_x, 0),
                (center_x, frame_height),
                (0, 0, 255),
                3
            )
   
            diagonal_start = (
            center_x - 1300,
            center_y + 1550
)

            diagonal_end = (
            center_x + 600,
            center_y + 100
)

            cv2.line(
                annotated_frame,
                diagonal_start,
                diagonal_end,
                (0, 0, 255),
                3
            )
  
            dx = diagonal_end[0] - diagonal_start[0]
            dy = diagonal_end[1] - diagonal_start[1]

            if dx != 0:

          
                t = (
                    center_x - diagonal_start[0]
                ) / dx

                intersection_y = int(
                    diagonal_start[1] + t * dy
                )

                intersection_x = center_x

                cv2.circle(
                    annotated_frame,
                    (
                        intersection_x,
                        intersection_y
                    ),
                    10,
                    (0, 0, 255),
                    -1
                )


                if (
                    x1 <= intersection_x <= x2
                    and
                    y1 <= intersection_y <= y2
                ):

                    filling_status = (
                        "DOLUM GERÇEKLEŞİYOR"
                    )

                else:

                    filling_status = (
                        "DOLUM GERÇEKLEŞMİYOR"
                    )

           

    cv2.putText(
        annotated_frame,
        filling_status,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        2.0,
        (0, 255, 0)
        if filling_status == "DOLUM GERÇEKLEŞİYOR"
        else (0, 0, 255),
        3
    )

    cv2.namedWindow(
        "Bellows Detection",
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        "Bellows Detection",
        640,
        360
    )

    cv2.imshow(
        "Bellows Detection",
        annotated_frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()