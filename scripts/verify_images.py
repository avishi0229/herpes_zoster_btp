import pandas as pd
from pathlib import Path

BASE_DIR = Path(r"C:\Users\avish\Desktop\scin_dataset")

CSV_FILE = BASE_DIR / "scin_hz_binary_final.csv"
IMAGE_DIR = BASE_DIR / "dataset" / "images"

df = pd.read_csv(CSV_FILE)

image_columns = [
    "image_1_path",
    "image_2_path",
    "image_3_path"
]

# Collect all image paths
paths = set()

for col in image_columns:
    for path in df[col].dropna():
        paths.add(Path(path).name)

print("=" * 60)
print("FINAL IMAGE VERIFICATION")
print("=" * 60)

print("Expected unique images:", len(paths))

missing = []
existing = []

for filename in sorted(paths):

    image_file = IMAGE_DIR / filename

    if image_file.exists():
        existing.append(filename)
    else:
        missing.append(filename)

print("\nExisting:", len(existing))
print("Missing :", len(missing))

if missing:
    print("\nMISSING FILES:")
    for filename in missing:
        print(filename)

print("\n" + "=" * 60)

if len(existing) == len(paths):
    print("SUCCESS: ALL IMAGES ARE PRESENT")
else:
    print("WARNING: SOME IMAGES ARE MISSING")

print("=" * 60)