"""
Task 2: Create CSV from the all_repository table.

Output CSV columns:
REPOID, LANG, STARS, REPOURL
"""

from datasets import load_dataset
import csv

OUTPUT_CSV = "task2_all_repository.csv"


def main():
    # Load the all_repository split from the AIDev dataset
    ds = load_dataset("hao-li/AIDev", "all_repository", split="train")

    fieldnames = ["REPOID", "LANG", "STARS", "REPOURL"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in ds:
            writer.writerow(
                {
                    "REPOID": row.get("id", ""),
                    "LANG": row.get("language", ""),
                    "STARS": row.get("stars", ""),
                    "REPOURL": row.get("url", ""),
                }
            )

    print(f"Task 2 complete. Wrote {len(ds)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
