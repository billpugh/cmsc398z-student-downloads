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
