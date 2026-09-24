import pandas as pd
from pathlib import Path

BASE = Path(r"C:\Users\avish\Desktop\scin_dataset")
IMAGE_DIR = BASE / "dataset" / "images"

splits = {
    "train": pd.read_csv(BASE / "train.csv"),
    "validation": pd.read_csv(BASE / "validation.csv"),
    "test": pd.read_csv(BASE / "test.csv")
}

image_cols = ["image_1_path", "image_2_path", "image_3_path"]

all_images = {}

for split_name, df in splits.items():

    images = set()

    for col in image_cols:
        for path in df[col].dropna():
            images.add(Path(path).name)

    all_images[split_name] = images

    missing = [
        img for img in images
        if not (IMAGE_DIR / img).exists()
    ]

    print(f"\n{split_name.upper()}")
    print("Cases:", df["case_id"].nunique())
    print("Images:", len(images))
    print("Missing:", len(missing))

print("\n" + "=" * 60)
print("IMAGE LEAKAGE CHECK")
print("=" * 60)

print("Train ∩ Validation:",
      len(all_images["train"] & all_images["validation"]))

print("Train ∩ Test:",
      len(all_images["train"] & all_images["test"]))

print("Validation ∩ Test:",
      len(all_images["validation"] & all_images["test"]))

print("=" * 60)