"""
Task 3: Create CSV from the pr_task_type table.

Output CSV columns:
PRID, PRTITLE, PRREASON, PRTYPE, CONFIDENCE
"""

from datasets import load_dataset
import csv

OUTPUT_CSV = "task3_pr_task_type.csv"


def main():
    # Load the pr_task_type split from the AIDev dataset
    ds = load_dataset("hao-li/AIDev", "pr_task_type", split="train")

    fieldnames = ["PRID", "PRTITLE", "PRREASON", "PRTYPE", "CONFIDENCE"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in ds:
            writer.writerow(
                {
                    "PRID": row.get("id", ""),
                    "PRTITLE": row.get("title", ""),
                    "PRREASON": row.get("reason", ""),
                    "PRTYPE": row.get("type", ""),
                    "CONFIDENCE": row.get("confidence", ""),
                }
            )

    print(f"Task 3 complete. Wrote {len(ds)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
