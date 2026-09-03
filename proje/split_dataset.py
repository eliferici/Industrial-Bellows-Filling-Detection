import os
import random
import shutil

IMAGE_DIR = "images"
LABEL_DIR = "labels"

TRAIN_IMAGE_DIR = "images/train"
VAL_IMAGE_DIR = "images/val"

TRAIN_LABEL_DIR = "labels/train"
VAL_LABEL_DIR = "labels/val"

os.makedirs(TRAIN_IMAGE_DIR, exist_ok=True)
os.makedirs(VAL_IMAGE_DIR, exist_ok=True)
os.makedirs(TRAIN_LABEL_DIR, exist_ok=True)
os.makedirs(VAL_LABEL_DIR, exist_ok=True)

images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

random.seed(42)
random.shuffle(images)

split_index = int(len(images) * 0.8)

train_images = images[:split_index]
val_images = images[split_index:]

for image_name in train_images:

    label_name = os.path.splitext(image_name)[0] + ".txt"

    shutil.move(
        os.path.join(IMAGE_DIR, image_name),
        os.path.join(TRAIN_IMAGE_DIR, image_name)
    )

    shutil.move(
        os.path.join(LABEL_DIR, label_name),
        os.path.join(TRAIN_LABEL_DIR, label_name)
    )


for image_name in val_images:

    label_name = os.path.splitext(image_name)[0] + ".txt"

    shutil.move(
        os.path.join(IMAGE_DIR, image_name),
        os.path.join(VAL_IMAGE_DIR, image_name)
    )

    shutil.move(
        os.path.join(LABEL_DIR, label_name),
        os.path.join(VAL_LABEL_DIR, label_name)
    )

print(f"Toplam görüntü: {len(images)}")
print(f"Train: {len(train_images)}")
print(f"Validation: {len(val_images)}")
print("Dataset bölme işlemi tamamlandı.")