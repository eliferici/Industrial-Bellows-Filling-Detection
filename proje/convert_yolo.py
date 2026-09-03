import os
import xml.etree.ElementTree as ET

XML_FILE = "annotations2.xml"

IMAGE_DIR = "images2"

LABEL_DIR = "labels2"

CLASS_NAMES = {
    "truck": 0,
    "bellows": 1,
    "cover_open": 2,
    "cover_closed": 3
}

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LABEL_DIR, exist_ok=True)

tree = ET.parse(XML_FILE)
root = tree.getroot()

for image in root.findall(".//image"):

    image_name = image.get("name")
    image_width = int(image.get("width"))
    image_height = int(image.get("height"))

    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(LABEL_DIR, label_name)

    labels = []

    # BOX'LAR
    for box in image.findall("box"):

        class_name = box.get("label")

        if class_name not in CLASS_NAMES:
            continue

        class_id = CLASS_NAMES[class_name]

        xtl = float(box.get("xtl"))
        ytl = float(box.get("ytl"))
        xbr = float(box.get("xbr"))
        ybr = float(box.get("ybr"))

        x_center = ((xtl + xbr) / 2) / image_width
        y_center = ((ytl + ybr) / 2) / image_height

        box_width = (xbr - xtl) / image_width
        box_height = (ybr - ytl) / image_height

        labels.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} "
            f"{box_width:.6f} {box_height:.6f}"
        )

    # ELLIPSE'LER
    for ellipse in image.findall("ellipse"):

        class_name = ellipse.get("label")

        if class_name not in CLASS_NAMES:
            continue

        class_id = CLASS_NAMES[class_name]

        cx = float(ellipse.get("cx"))
        cy = float(ellipse.get("cy"))
        rx = float(ellipse.get("rx"))
        ry = float(ellipse.get("ry"))

        xtl = cx - rx
        ytl = cy - ry
        xbr = cx + rx
        ybr = cy + ry

        x_center = ((xtl + xbr) / 2) / image_width
        y_center = ((ytl + ybr) / 2) / image_height

        box_width = (xbr - xtl) / image_width
        box_height = (ybr - ytl) / image_height

        labels.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} "
            f"{box_width:.6f} {box_height:.6f}"
        )

    with open(label_path, "w") as f:
        f.write("\n".join(labels))

    print(f"Tamamlandı: {image_name}")

print("YOLO dönüşümü tamamlandı!")