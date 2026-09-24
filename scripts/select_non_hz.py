import pandas as pd

# ============================================================
# LOAD HARD NEGATIVE CANDIDATES
# ============================================================

INPUT_FILE = "scin_non_hz_hard_negative_candidates.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("SELECTING FINAL NON-HZ CASES")
print("=" * 70)

# ============================================================
# CONDITIONS
# ============================================================

conditions = [
    "Herpes Simplex",
    "Impetigo",
    "Folliculitis",
    "Allergic Contact Dermatitis",
    "Irritant Contact Dermatitis",
    "Acute dermatitis, NOS",
    "Urticaria",
    "Insect Bite"
]

CASES_PER_CONDITION = 7

# ============================================================
# SELECT CASES
# ============================================================

selected_parts = []

for condition in conditions:

    candidates = df[
        df["dominant_condition"] == condition
    ].copy()

    print(f"\n{condition}")
    print(f"Available cases: {len(candidates)}")

    # Fixed random seed = reproducible selection
    selected = candidates.sample(
        n=CASES_PER_CONDITION,
        random_state=42
    )

    selected_parts.append(selected)

# ============================================================
# COMBINE
# ============================================================

selected_df = pd.concat(
    selected_parts,
    ignore_index=True
)

# ============================================================
# ADD BINARY LABEL
# ============================================================

selected_df["label"] = 0

# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE = "scin_non_hz_selected_56_cases.csv"

selected_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL NON-HZ SELECTION")
print("=" * 70)

print(
    selected_df["dominant_condition"]
    .value_counts()
)

print("\nTotal cases:")
print(selected_df["case_id"].nunique())

print("\nTotal images:")
print(selected_df["num_images_actual"].sum())

print("\nSaved:")
print(OUTPUT_FILE)

print("=" * 70)