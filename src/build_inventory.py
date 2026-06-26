from pathlib import Path
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent

FEATURES_DIR = PROJECT_DIR / "analysis"

OUTPUT_CSV = FEATURES_DIR / "embryo_inventory.csv"


feature_files = sorted(
    FEATURES_DIR.rglob("*features*.csv")
)

if len(feature_files) == 0:
    print("\nNo feature CSV files found.")
    print("Check your analysis directory structure.")
    raise SystemExit

print(f"\nFound {len(feature_files)} feature files\n")


inventory = []

for file in feature_files:

    try:

        df = pd.read_csv(file)

       
        # Try to infer genotype and embryo name

        parts = file.parts

        genotype = "unknown"
        embryo = file.stem

        if len(parts) >= 2:
            genotype = file.parent.name

        # Find frame column

        frame_col = None

        for col in df.columns:

            if col.lower() in [
                "frame",
                "frames",
                "time",
                "t"
            ]:
                frame_col = col
                break

        if frame_col is None:

            print(
                f"Skipping {file.name}: no frame column"
            )

            continue

        n_frames = df[frame_col].nunique()

        first_frame = int(df[frame_col].min())
        last_frame = int(df[frame_col].max())

        inventory.append(
            {
                "genotype": genotype,
                "embryo": embryo,
                "n_frames": n_frames,
                "first_frame": first_frame,
                "last_frame": last_frame,
                "file": str(file)
            }
        )

    except Exception as e:

        print(f"Failed: {file}")
        print(e)

inventory_df = pd.DataFrame(inventory)

if len(inventory_df) == 0:

    print("\nNo valid feature tables found.")
    raise SystemExit

inventory_df = inventory_df.sort_values(
    ["genotype", "embryo"]
)

inventory_df.to_csv(
    OUTPUT_CSV,
    index=False
)

print("\n===================================")
print("EMBRYO INVENTORY")
print("===================================\n")

print(inventory_df)

print("\n===================================")
print("GENOTYPE COUNTS")
print("===================================\n")

counts = (
    inventory_df.groupby("genotype")
    .size()
    .sort_values(ascending=False)
)

print(counts)

print("\n===================================")
print("FRAME RANGE CHECK")
print("===================================\n")

frame_summary = (
    inventory_df.groupby("genotype")
    .agg(
        embryos=("embryo", "count"),
        min_frames=("n_frames", "min"),
        max_frames=("n_frames", "max"),
        first_frame=("first_frame", "min"),
        last_frame=("last_frame", "max")
    )
)

print(frame_summary)

print("\nSaved:")
print(OUTPUT_CSV)
