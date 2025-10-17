import argparse
import re
import sys
import csv
import time

import sqlite_utils
import llm


def extract_sql(text: str) -> str:
    """Try to extract SQL from a model response.

    - Prefer fenced code blocks (``` or ```sql).
    - Otherwise strip common leading commentary like 'SQL:'.
    - Fall back to returning the full response.
    """
    if not text:
        return ""

    # Look for fenced code block
    m = re.search(r"```(?:sql)?\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # If there's an inline code fence `...`
    m = re.search(r"`{1,3}\s*(SELECT|WITH|INSERT|UPDATE|DELETE|CREATE|PRAGMA)", text, flags=re.IGNORECASE)
    if m:
        # try to pull from first backtick to the last backtick
        parts = re.split(r"`{1,3}", text)
        # find a part that looks like SQL
        for part in parts:
            if re.match(r"^\s*(SELECT|WITH|INSERT|UPDATE|DELETE|CREATE|PRAGMA)", part, flags=re.IGNORECASE):
                return part.strip()

    # Remove a leading "SQL:" or "SQL -"
    m = re.search(r"SQL[:\-\s]\s*(.*)", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # As a last resort, return the whole text
    return text.strip()


def prompt_to_sql(model, schema: str, question: str, system_msg: str) -> str:
    prompt = f"Schema:\n\n{schema}\n\nQuestion:\n\n{question}"
    resp = model.prompt(prompt, system=system_msg).text()
    return extract_sql(resp)


def main():
    parser = argparse.ArgumentParser(
        description="Simple text-to-SQL CLI backed by an LLM and sqlite-utils."
    )
    parser.add_argument("db", help="Path to the sqlite database file")
    parser.add_argument("question", help="Natural language question to convert to SQL")
    parser.add_argument(
        "--schema",
        "-s",
        help="Path to a .sql file containing the schema to send to the model. If omitted, the DB schema is used.",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="gpt-5-mini",
        help="LLM model to use (default: gpt-5-mini)",
    )
    parser.add_argument(
        "--no-exec",
        action="store_true",
        help="Only print the SQL generated; do not try to execute it against the DB",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=200,
        help="Maximum number of rows to fetch and write when executing (default: 200)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output CSV file for query results (default: results-<timestamp>.csv)",
    )

    args = parser.parse_args()

    # load DB
    db = sqlite_utils.Database(args.db)

    # load schema
    if args.schema:
        with open(args.schema, "r", encoding="utf-8") as fh:
            schema = fh.read()
    else:
        schema = db.schema

    # prepare model
    model = llm.get_model(args.model)

    system_msg = "reply with SQLite SQL, not in markdown, just the SQL"

    # Get SQL from model
    sql = prompt_to_sql(model, schema, args.question, system_msg)
    if not sql:
        print("No SQL was produced by the model.", file=sys.stderr)
        sys.exit(1)

    print("---- Generated SQL ----")
    print(sql)
    print("-----------------------")

    if args.no_exec:
        sys.exit(0)

    # Try executing the SQL. IMPORTANT: We will only execute read-only queries.
    # Do not run statements that modify the database (CREATE, INSERT, UPDATE, DELETE, DROP, etc.)
    def try_execute(sql_text):
        sql_clean = sql_text.strip()
        # Determine whether this is a read-only query we will allow
        allow_prefixes = ("SELECT", "WITH", "PRAGMA")
        first_word = sql_clean.split(None, 1)[0].upper() if sql_clean else ""
        if not sql_clean.upper().startswith(allow_prefixes):
            # Refuse to automatically execute any statement that could modify the DB.
            return False, Exception(
                "Refusing to execute non-query SQL to avoid modifying the database. "
                "Only read-only queries (SELECT/WITH/PRAGMA) are allowed."
            )

        try:
            cur = db.conn.execute(sql_text)
            # fetch rows (up to max_rows)
            rows = cur.fetchmany(args.max_rows)
            columns = [d[0] for d in cur.description] if cur.description else []

            # determine output file
            if args.output:
                out_path = args.output
            else:
                # default to a timestamped file so repeated runs don't clobber each other
                ts = int(time.time())
                out_path = f"results-{ts}.csv"

            # Write CSV
            with open(out_path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.writer(fh)
                if columns:
                    writer.writerow(columns)
                for r in rows:
                    # Convert any bytes objects to strings for CSV compatibility
                    clean_row = []
                    for v in r:
                        if isinstance(v, (bytes, bytearray)):
                            try:
                                clean_row.append(v.decode("utf-8"))
                            except Exception:
                                clean_row.append(str(v))
                        else:
                            clean_row.append(v)
                    writer.writerow(clean_row)

            # Print summary to stdout
            print(f"Query executed successfully. Wrote {len(rows)} rows to {out_path}")
            if len(rows) == args.max_rows:
                print(f"... (fetched {args.max_rows} rows; limit reached)")
            return True, None
        except Exception as e:
            return False, e

    ok, err = try_execute(sql)
    if ok:
        return

    # If we get here, initial execution failed; report and attempt one repair pass (still read-only)
    print("Initial execution failed with error:", err, file=sys.stderr)
    repair_prompt = (
        f"Schema:\n\n{schema}\n\n"
        f"Question:\n\n{args.question}\n\n"
        "The SQL you produced failed when executed against the database.\n"
        f"SQL that failed:\n\n{sql}\n\n"
        f"Error:\n\n{err}\n\n"
        "Please return corrected SQLite SQL only (no markdown). Only return a read-only query "
        "(SELECT/WITH/PRAGMA). Do not return any statements that modify the database."
    )
    resp = model.prompt(repair_prompt, system=system_msg).text()
    sql2 = extract_sql(resp)
    print("---- Repaired SQL ----")
    print(sql2)
    print("----------------------")
    if not sql2:
        print("Model did not produce corrected SQL.", file=sys.stderr)
        sys.exit(1)

    ok2, err2 = try_execute(sql2)
    if ok2:
        return

    print("Repaired SQL still failed with error:", err2, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
