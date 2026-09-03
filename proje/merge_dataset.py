import os
import shutil
import random

# =========================
# ESKİ DATASET
# =========================

OLD_IMAGES_TRAIN = "images/train"
OLD_IMAGES_VAL = "images/val"

OLD_LABELS_TRAIN = "labels/train"
OLD_LABELS_VAL = "labels/val"


# =========================
# YENİ DATASET
# =========================

NEW_IMAGES = "images2"
NEW_LABELS = "labels2"


# =========================
# YENİ BİRLEŞTİRİLMİŞ DATASET
# =========================

DATASET_IMAGES = "dataset/images"
DATASET_LABELS = "dataset/labels"

TRAIN_IMAGES = "dataset/images/train"
VAL_IMAGES = "dataset/images/val"

TRAIN_LABELS = "dataset/labels/train"
VAL_LABELS = "dataset/labels/val"


# Eski oluşturulmuş dataset varsa temizle
if os.path.exists("dataset"):
    shutil.rmtree("dataset")


# Klasörleri oluştur
for folder in [
    TRAIN_IMAGES,
    VAL_IMAGES,
    TRAIN_LABELS,
    VAL_LABELS
]:
    os.makedirs(folder, exist_ok=True)


# Birleştirilecek görüntü ve label listesi
all_data = []


# =========================
# ESKİ DATASETİ EKLE
# =========================

def add_old_dataset(image_dir, label_dir):

    for image_name in os.listdir(image_dir):

        if not image_name.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        image_path = os.path.join(image_dir, image_name)

        label_name = os.path.splitext(image_name)[0] + ".txt"
        label_path = os.path.join(label_dir, label_name)

        if not os.path.exists(label_path):
            print(f"ESKI DATASET - Etiket yok: {image_name}")
            continue

        all_data.append(
            (image_path, label_path, image_name)
        )


add_old_dataset(
    OLD_IMAGES_TRAIN,
    OLD_LABELS_TRAIN
)

add_old_dataset(
    OLD_IMAGES_VAL,
    OLD_LABELS_VAL
)


# =========================
# YENİ DATASETİ EKLE
# =========================

for image_name in os.listdir(NEW_IMAGES):

    if not image_name.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):
        continue

    image_path = os.path.join(NEW_IMAGES, image_name)

    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(NEW_LABELS, label_name)

    # Yeni görüntülere NEW_ ekliyoruz
    # Böylece frame_00001.jpg çakışması olmaz.
    new_image_name = "NEW_" + image_name
    new_label_name = "NEW_" + label_name

    if not os.path.exists(label_path):

        print(
            f"UYARI - Yeni dataset'te etiket yok: {image_name}"
        )

        # Etiketsiz görüntüyü de koruyoruz.
        # Boş txt dosyası oluşturacağız.
        all_data.append(
            (image_path, None, new_image_name)
        )

    else:

        all_data.append(
            (image_path, label_path, new_image_name)
        )


# =========================
# TOPLAM DATASET
# =========================

random.seed(42)
random.shuffle(all_data)

total = len(all_data)

split_index = int(total * 0.8)

train_data = all_data[:split_index]
val_data = all_data[split_index:]


# =========================
# DOSYALARI KOPYALA
# =========================

def copy_data(data_list, image_destination, label_destination):

    for image_path, label_path, image_name in data_list:

        # Görüntüyü kopyala
        shutil.copy2(
            image_path,
            os.path.join(image_destination, image_name)
        )

        # Label ismi
        label_name = os.path.splitext(image_name)[0] + ".txt"

        destination_label = os.path.join(
            label_destination,
            label_name
        )

        # Label varsa kopyala
        if label_path is not None:

            shutil.copy2(
                label_path,
                destination_label
            )

        # Label yoksa boş txt oluştur
        else:

            open(
                destination_label,
                "w"
            ).close()


copy_data(
    train_data,
    TRAIN_IMAGES,
    TRAIN_LABELS
)

copy_data(
    val_data,
    VAL_IMAGES,
    VAL_LABELS
)


# =========================
# SONUÇ
# =========================

print()
print("==============================")
print("DATASET BIRLESTIRILDI")
print("==============================")
print(f"Toplam görüntü : {total}")
print(f"Train          : {len(train_data)}")
print(f"Validation     : {len(val_data)}")
print("==============================")
print("Dataset hazır.")
