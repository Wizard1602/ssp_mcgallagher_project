"""
Task 5: Create CSV combining pull request info, task type, and a SECURITY flag.

Inputs (CSV outputs from previous tasks):
- Task 1: task1_all_pull_request.csv  -> PR-level info (ID, AGENT, TITLE, BODY)
- Task 2: task2_all_repository.csv    -> Repo-level info (LANG, STARS, etc.)
- Task 3: task3_pr_task_type.csv      -> PR TYPE and CONFIDENCE
- Task 4: task4_pr_commit_details.csv -> Commit-level info (DIFF, FILES, etc.)

Per the project specification, the final CSV must contain:
ID, AGENT, TYPE, CONFIDENCE, SECURITY

Only the Task 1 and Task 3 outputs actually contain the fields needed
for these five columns (ID/AGENT from Task 1, TYPE/CONFIDENCE from Task 3).
Task 2 and Task 4 CSVs are still required outputs but their columns are
not used directly in this aggregation.
"""

import csv
import re
from pathlib import Path

# Input CSVs from Tasks 1–4
TASK1_CSV = "task1_all_pull_request.csv"
TASK2_CSV = "task2_all_repository.csv"
TASK3_CSV = "task3_pr_task_type.csv"
TASK4_CSV = "task4_pr_commit_details.csv"

# Output CSV for Task 5
OUTPUT_CSV = "task5_security_summary.csv"


# Security-related keywords from the project instructions
SECURITY_KEYWORDS = [
    "race",
    "racy",
    "buffer",
    "overflow",
    "stack",
    "integer",
    "signedness",
    "underflow",
    "improper",
    "unauthenticated",
    "gain access",
    "permission",
    "cross site",
    "css",
    "xss",
    "denial service",
    "dos",
    "crash",
    "deadlock",
    "injection",
    "request forgery",
    "csrf",
    "xsrf",
    "forged",
    "security",
    "vulnerability",
    "vulnerable",
    "exploit",
    "attack",
    "bypass",
    "backdoor",
    "threat",
    "expose",
    "breach",
    "violate",
    "fatal",
    "blacklist",
    "overrun",
    "insecure",
]


def build_security_pattern():
    """
    Build a case-insensitive regex that matches any of the keywords
    in the text (title + body).
    """
    escaped_keywords = [re.escape(k) for k in SECURITY_KEYWORDS]
    pattern_str = "(" + "|".join(escaped_keywords) + ")"
    return re.compile(pattern_str, re.IGNORECASE)


def has_security_keyword(text, pattern):
    """
    Return 1 if any security keyword is found in text, else 0.
    """
    if not text:
        return 0
    if pattern.search(text):
        return 1
    return 0


def load_pr_type_info(task3_path):
    """
    Load Task 3 CSV into a dictionary mapping:
    PRID -> (PRTYPE, CONFIDENCE)

    This lets us look up type/confidence by pull request ID.
    """
    pr_info = {}
    with open(task3_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pr_id = row.get("PRID", "")
            pr_type = row.get("PRTYPE", "")
            confidence = row.get("CONFIDENCE", "")
            if pr_id:
                pr_info[pr_id] = (pr_type, confidence)
    return pr_info


def ensure_inputs_exist():
    """
    Ensure all four previous-task CSVs exist before proceeding.
    """
    for path in [TASK1_CSV, TASK2_CSV, TASK3_CSV, TASK4_CSV]:
        if not Path(path).is_file():
            raise FileNotFoundError(f"Missing required input CSV from previous tasks: {path}")


def main():
    # Make sure all previous-task CSVs are present
    ensure_inputs_exist()

    # Load TYPE and CONFIDENCE info from Task 3
    pr_type_map = load_pr_type_info(TASK3_CSV)

    # Build regex pattern for security keyword detection
    sec_pattern = build_security_pattern()

    fieldnames = ["ID", "AGENT", "TYPE", "CONFIDENCE", "SECURITY"]

    count = 0
    matched_pr_types = 0

    with open(TASK1_CSV, "r", encoding="utf-8") as f_in, open(
        OUTPUT_CSV, "w", newline="", encoding="utf-8"
    ) as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            pr_id = row.get("ID", "")
            agent = row.get("AGENTNAME", "")

            # Title and body for keyword scan
            title = row.get("TITLE", "") or ""
            body = row.get("BODYSTRING", "") or ""
            combined_text = f"{title} {body}"

            # Security flag (1/0)
            security_flag = has_security_keyword(combined_text, sec_pattern)

            # Look up type/confidence from Task 3
            pr_type = ""
            confidence = ""
            if pr_id in pr_type_map:
                pr_type, confidence = pr_type_map[pr_id]
                matched_pr_types += 1

            writer.writerow(
                {
                    "ID": pr_id,
                    "AGENT": agent,
                    "TYPE": pr_type,
                    "CONFIDENCE": confidence,
                    "SECURITY": security_flag,
                }
            )

            count += 1
            if count % 50000 == 0:
                print(f"Processed {count} pull requests...")

    print(f"Task 5 complete. Wrote {count} rows to {OUTPUT_CSV}")
    print(f"Number of PRs with type/confidence info: {matched_pr_types}")


if __name__ == "__main__":
    main()
