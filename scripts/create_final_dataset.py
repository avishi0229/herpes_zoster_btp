import pandas as pd

# ============================================================
# LOAD DATA
# ============================================================

hz = pd.read_csv(
    "scin_hz_high_confidence_with_images.csv"
)

non_hz = pd.read_csv(
    "scin_non_hz_selected_56_cases.csv"
)

# ============================================================
# LABELS
# ============================================================

hz["label"] = 1
hz["condition"] = "Herpes Zoster"

non_hz["label"] = 0

# dominant_condition already exists for Non-HZ
non_hz["condition"] = non_hz["dominant_condition"]

# ============================================================
# SELECT COMMON IMPORTANT COLUMNS
# ============================================================

columns = [
    "case_id",
    "label",
    "condition",

    "age_group",
    "sex_at_birth",
    "fitzpatrick_skin_type",

    "textures_raised_or_bumpy",
    "textures_flat",
    "textures_rough_or_flaky",
    "textures_fluid_filled",

    "body_parts_head_or_neck",
    "body_parts_arm",
    "body_parts_palm",
    "body_parts_back_of_hand",
    "body_parts_torso_front",
    "body_parts_torso_back",
    "body_parts_buttocks",
    "body_parts_leg",
    "body_parts_foot_top_or_side",
    "body_parts_foot_sole",

    "condition_symptoms_itching",
    "condition_symptoms_burning",
    "condition_symptoms_pain",

    "other_symptoms_fever",
    "other_symptoms_chills",
    "other_symptoms_fatigue",

    "condition_duration",

    "image_1_path",
    "image_2_path",
    "image_3_path",

    "num_images"
]

# Keep only columns that exist
columns_hz = [c for c in columns if c in hz.columns]
columns_non = [c for c in columns if c in non_hz.columns]

hz_final = hz[columns_hz].copy()
non_hz_final = non_hz[columns_non].copy()

# ============================================================
# COMBINE
# ============================================================

final = pd.concat(
    [hz_final, non_hz_final],
    ignore_index=True
)

# ============================================================
# REMOVE DUPLICATE CASES
# ============================================================

final = final.drop_duplicates(
    subset=["case_id"]
)

# ============================================================
# SHUFFLE CASES
# ============================================================

final = final.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ============================================================
# SAVE
# ============================================================

output = "scin_hz_binary_final.csv"

final.to_csv(
    output,
    index=False
)

# ============================================================
# SUMMARY
# ============================================================

print("=" * 70)
print("FINAL SCIN HZ BINARY DATASET")
print("=" * 70)

print("\nCases:")
print(final["case_id"].nunique())

print("\nClass distribution:")
print(final["label"].value_counts())

print("\nCondition distribution:")
print(final["condition"].value_counts())

print("\nImages:")
print(final["num_images"].sum())

print("\nSaved:")
print(output)

print("=" * 70)