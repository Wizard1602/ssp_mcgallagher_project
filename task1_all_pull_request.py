"""
Task 1: Create CSV from the all_pull_request table.

Output CSV columns (exactly as required):
TITLE, ID, AGENTNAME, BODYSTRING, REPOID, REPOURL
"""

from datasets import load_dataset
import csv

OUTPUT_CSV = "task1_all_pull_request.csv"


def main():
    # This will download the dataset the first time and cache it locally.
    ds = load_dataset("hao-li/AIDev", "all_pull_request", split="train")

    fieldnames = ["TITLE", "ID", "AGENTNAME", "BODYSTRING", "REPOID", "REPOURL"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in ds:
            writer.writerow(
                {
                    "TITLE": row.get("title", ""),
                    "ID": row.get("id", ""),
                    "AGENTNAME": row.get("agent", ""),
                    "BODYSTRING": row.get("body", "") or "",
                    "REPOID": row.get("repo_id", ""),
                    "REPOURL": row.get("repo_url", ""),
                }
            )

    print(f"Task 1 complete. Wrote {len(ds)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
