# Building a text to SQL tool

We're going to build something *genuinely useful*. Weirdly enough, this is a "hello world" exercise for prompt engineering.

Ask a question of your database in English, get a response from a custom SQL query written by the LLM.

## The UMD course database

Bill Pugh developed a project to scrap the the Testudo web site to collect data about UMD courses.

Download and save the course database from [https://www.cs.umd.edu/class/fall2025/cmsc398z/files/umd-202508.db](https://www.cs.umd.edu/class/fall2025/cmsc398z/files/umd-202508.db)

The schema for this database is defined in [umd-schema.sql](umd-schema.sql). There are two Mermaid diagrams for it, one that simplified the database in [schema_diagram.md](schema_diagram.md), and a complete diagram in [schema_diagram_complete.md](schema_diagram_complete.md). The database schema is designed to manage data for multiple terms, and allow scraping data for a term and department multiple times to keep track of changes in number of seats, and check for added or dropped courses or sections.

## Prototyping against the UMD course database

We're going to examine the UMD course database, and prototype against it using the `sqlite-utils` CLI tool:

```bash
sqlite-utils schema umd-202508.db
```
Let's write that to a file:

```bash
sqlite-utils schema umd-202508.db > schema.sql
```

Now we can feed it to LLM and write our first query:

```bash
llm -f schema.sql \
  -s "reply with sqlite SQL" \
  "how many courses are there?"
```

I got back

```
```sql
To get counts, run one of these SQLite queries depending on what you mean by "how many courses":

Total courses (rows in course_info):
SELECT COUNT(*) AS total_courses FROM course_info;
...
Courses per department:
SELECT department, COUNT(*) AS courses FROM course_info GROUP BY department ORDER BY courses DESC;
...
```

So, lets's be a little more specific

```bash
llm -f schema.sql -s "reply with sqlite SQL" \
"list the number of courses for each department for the 202508 term"
```

which returns

```sql
SELECT department,
       COUNT(*) AS course_count
FROM course_info
WHERE term_id = '202508'
GROUP BY department
ORDER BY course_count DESC, department;
```

Note that it doesn't always come back as pure sql, the llm might return several options with descriptions, as above, or as a markdown LLM with the SQL wrapped it in a fenced code block.
We could ask it not to, but we can also use the `--extract` flag to extract the SQL from the response if it is wrapped in a code block.

```bash
llm -f schema.sql \
  -s "reply with sqlite SQL" \
  --extract \
  "list the number of courses for each department for the 202508 term"
```

Let's run that query in the most diabolical way possible:

```bash
sqlite-utils umd-202508.db "$(llm -f schema.sql \
  -s 'reply with sqlite SQL' \
  --extract \
  'list the number of courses for each department for the 202508 term')"
```

## A more detailed schema

We can just use the schema that can be extracted from the database. But in my work on the Testudo scanner, I created a more detailed schema [umd-schema.sql](umd-schema.sql), that contains lots of additional documentation and examples. When trying to generate sql for a query, either with an LLM or manually, using that more detailed schema may prove useful. 

## Turning that into a Python function

Let's upgrade our hacky CLI prototype into a Python function.

```python
import sqlite_utils
import llm
import csv
import sys

model = llm.get_model("gpt-5-mini")

def text_to_sql(db: sqlite_utils.Database, question: str) -> str:
    """Convert a prompt to SQL using the LLM."""
    prompt = "Schema:\n\n{}\n\nQuestion:\n\n{}".format(
        db.schema, question
    )
    return model.prompt(
        prompt,
        system="reply with SQLite SQL, not in markdown, just the SQL",
    ).text()

db = sqlite_utils.Database("umd-202508.db")

sql = text_to_sql(db, "list the number of courses for each department for the 202508 term")

# Execute and print CSV
cursor = db.conn.execute(sql)
columns = [desc[0] for desc in cursor.description]  # column names

writer = csv.writer(sys.stdout)
writer.writerow(columns)

for row in cursor:
    # row is an sqlite3.Row or tuple-like; convert values to strings and handle NULL
    writer.writerow([("" if v is None else v) for v in row])
```

Notes:

- This uses db.conn.execute(sql) to get a cursor with .description (column names) and iterate rows.
- csv.writer writes rows directly to stdout; you can change to write to a file by opening a file and passing that to csv.writer instead of sys.stdout.

## Upgrading that to a CLI tool

Now that we have this working, let's turn it into a small CLI tool using `argparse` from the Python standard library. It should allow a database other than umd-202508.db to be specified, and allow a separate schema to be specified, rather than just using the one generated from the database.

```python
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
```


Here's a fun note: the above block, usage examples and notes just said "FILL ME" and then I ran this command:

```bash
llm -m gpt-5-mini -f text-to-sql.md -s 'Write the code for the FILL ME bit'
```

## Ways to make this better

This is the most basic version of this, but it works pretty well!

Some ways we could make this better:

- **Examples**. The single most powerful prompt engineering trick is to give the LLM illustrative examples of what you are trying to achieve. A small number of carefully selected examples of questions and the expected SQL answer can radically improve the results.
- **Column values**. A common failure case for text to SQL is when the question is e.g. "How many schools are in California?" and the model queries for `where state = 'California'` when it should have queried for `where state = 'CA'`. Feeding in some example value from each column can be all the model needs to get it right.
- **Data documentation**. Just like a real data analyst, the more information you can feed the model the better.
- **Explaining errors**.  You can use `EXPLAIN ...` for a cheap validation of the query without running the whole thing. EXPLAIN will also tell you whether the indices in the database allow for efficient execution of the query.
