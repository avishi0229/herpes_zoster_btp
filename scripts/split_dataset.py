import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# LOAD FINAL DATASET
# ============================================================

INPUT_FILE = "scin_hz_binary_final.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("CASE-LEVEL DATASET SPLIT")
print("=" * 70)

print("Total cases:", df["case_id"].nunique())

# ============================================================
# MAKE SURE ONE ROW = ONE CASE
# ============================================================

case_df = df.drop_duplicates(
    subset=["case_id"]
).copy()

# ============================================================
# FIRST SPLIT
# 70% TRAIN
# 30% TEMP
# ============================================================

train_cases, temp_cases = train_test_split(
    case_df,
    test_size=0.30,
    random_state=42,
    stratify=case_df["label"]
)

# ============================================================
# SECOND SPLIT
# TEMP → 50% VALIDATION / 50% TEST
#
# Therefore:
# TRAIN = 70%
# VAL   = 15%
# TEST  = 15%
# ============================================================

val_cases, test_cases = train_test_split(
    temp_cases,
    test_size=0.50,
    random_state=42,
    stratify=temp_cases["label"]
)

# ============================================================
# GET CASE IDS
# ============================================================

train_ids = set(train_cases["case_id"])
val_ids = set(val_cases["case_id"])
test_ids = set(test_cases["case_id"])

# ============================================================
# CHECK FOR LEAKAGE
# ============================================================

print("\nChecking case overlap...")

print(
    "Train ∩ Validation:",
    len(train_ids & val_ids)
)

print(
    "Train ∩ Test:",
    len(train_ids & test_ids)
)

print(
    "Validation ∩ Test:",
    len(val_ids & test_ids)
)

# ============================================================
# CREATE SPLIT DATAFRAMES
# ============================================================

train_df = df[df["case_id"].isin(train_ids)].copy()
val_df = df[df["case_id"].isin(val_ids)].copy()
test_df = df[df["case_id"].isin(test_ids)].copy()

# ============================================================
# SHUFFLE
# ============================================================

train_df = train_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

val_df = val_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

test_df = test_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ============================================================
# SAVE
# ============================================================

train_df.to_csv(
    "train.csv",
    index=False
)

val_df.to_csv(
    "validation.csv",
    index=False
)

test_df.to_csv(
    "test.csv",
    index=False
)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SPLIT SUMMARY")
print("=" * 70)

for name, data in [
    ("TRAIN", train_df),
    ("VALIDATION", val_df),
    ("TEST", test_df)
]:

    print(f"\n{name}")

    print("Cases:",
          data["case_id"].nunique())

    print("Images:",
          len([
              x
              for col in [
                  "image_1_path",
                  "image_2_path",
                  "image_3_path"
              ]
              for x in data[col].dropna()
          ]))

    print("Class distribution:")

    print(
        data
        .drop_duplicates("case_id")["label"]
        .value_counts()
        .sort_index()
    )

print("\nFiles created:")
print("train.csv")
print("validation.csv")
print("test.csv")

print("\nCase leakage check complete.")
print("=" * 70)