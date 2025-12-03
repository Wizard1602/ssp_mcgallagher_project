"""
Task 4: Create CSV from the pr_commit_details table.

Output CSV columns:
PRID, PRSHA, PRCOMMITMESSAGE, PRFILE, PRSTATUS,
PRADDS, PRDELSS, PRCHANGECOUNT, PRDIFF

PRDIFF is taken from 'patch' with special characters removed
to avoid string encoding / CSV parsing issues.
"""

from datasets import load_dataset
import csv
import string

OUTPUT_CSV = "task4_pr_commit_details.csv"


def clean_patch(patch_value):
    """
    Clean the diff/patch string by:
    - Converting None to empty string
    - Removing non-printable characters
    This keeps normal text, spaces, tabs, and newlines.
    """
    if patch_value is None:
        return ""

    text = str(patch_value)

    # string.printable contains digits, letters, punctuation, whitespace
    allowed = set(string.printable)
    cleaned = "".join(ch for ch in text if ch in allowed)

    return cleaned


def main():
    # Load the pr_commit_details split from the AIDev dataset
    ds = load_dataset("hao-li/AIDev", "pr_commit_details", split="train")

    fieldnames = [
        "PRID",
        "PRSHA",
        "PRCOMMITMESSAGE",
        "PRFILE",
        "PRSTATUS",
        "PRADDS",
        "PRDELSS",
        "PRCHANGECOUNT",
        "PRDIFF",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for row in ds:
            writer.writerow(
                {
                    "PRID": row.get("pr_id", ""),
                    "PRSHA": row.get("sha", ""),
                    "PRCOMMITMESSAGE": row.get("message", ""),
                    "PRFILE": row.get("filename", ""),
                    "PRSTATUS": row.get("status", ""),
                    "PRADDS": row.get("additions", ""),
                    "PRDELSS": row.get("deletions", ""),
                    "PRCHANGECOUNT": row.get("changes", ""),
                    "PRDIFF": clean_patch(row.get("patch", "")),
                }
            )

            count += 1
            if count % 10000 == 0:  # optional: print only every 10k to avoid spamming
                print(f"Processed {count} rows...")

    print(f"Task 4 complete. Wrote {len(ds)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
