# Prompting from Python

LLM is also [a Python library](https://llm.datasette.io/en/latest/python-api.html). Let's run a prompt from Python:

```python
import llm
model = llm.get_model("gpt-5-mini")
response = model.prompt(
    "A joke about a walrus who lost his shoes"
)
print(response.text())
```

LLM defaults to picking up keys you have already configured. You can pass an explicit API key using the `key=` argument like this:

```python
response = model.prompt("Say hi", key="sk-...")
```

## Streaming

You can stream responses in Python like this:

```python
for chunk in model.prompt(
    "A joke about a terrapin who rides a bicycle",
    stream=True):
    print(chunk, end="", flush=True)
```

## Using attachments

Use `llm.Attachment` to attach files to your prompt:

```python
response = model.prompt(
    "Describe this image",
    attachments=[
        llm.Attachment(
            url="https://www.cs.umd.edu/class/fall2025/cmsc398z/files/week5a.jpg",
        )
    ]
)
print(response.text())
```

## Using system prompts

System prompts become particularly important once you start building applications on top of LLMs.

Let's write a function to translate English to Spanish:

```python
def translate_to_spanish(text):
    model = llm.get_model("gpt-5-mini")
    response = model.prompt(
        text,
        system="Translate this to Spanish"
    )
    return response.text()

# And try it out:
print(translate_to_spanish("What is the best thing about a terrapin?"))
```

We're writing software with LLMs!

## Specifying schemas

Here is a function that takes a system prompt, a list of attachments and a schema specified in llm's mini-DSL format, and returns the result.

```python
def extract_data(model: str, system:str, attachments:llm.Attachment,  schema: str, multi: bool = False):
    full_schema = llm.schema_dsl(schema, multi=multi)
    model = llm.get_model(model)
    response = model.prompt(
        system=system,
        attachments=attachments,
        schema=full_schema
    )
    return response
```

## Formatting json

This code takes a response from an llm, parses the output as json, and then converts the json back to formatted multiline text. If you wish to modify the json, such as adding additional properties, you could do so between these two lines:

```python
    parsed = json.loads(response.text())
    data = json.dumps(parsed, indent=4)
```

## Logging when calling from python

I was at first confused by the fact that the prompting I was doing from inside python code wasn't being logged. Searching a manual for why something doesn't happen can often be challenging. Also, defining a tool named `llm` makes it hard to do web searches for information about how to use that tool. Kind of like calling a hotel in College Park "The Hotel".

So I just downloaded the source code for LLM, and asked Claude to examine the source to figure out why logging wasn't happening when prompting was done from python code. It gave me the answer:

**Logging is NOT automatic when using the Python API** - you must explicitly call `response.log_to_db(db)` to log requests to the database.

### Why the difference?

1. **CLI behavior**: The CLI automatically logs all prompts/responses to the database (unless you use `--no-log` or have turned logging off with `llm logs off`)

2. **Python API behavior**: When using the Python library directly, logging is **manual and opt-in**. You need to:
   - Get a database connection
   - Call `response.log_to_db(db)` explicitly

### How to log from Python

Here's how to log your Python API requests:

```python
import llm
import sqlite_utils

# Get your model and make a request
model = llm.get_model("gpt-4o-mini")
response = model.prompt("Five surprising names for a pet terripin")

# Force evaluation of the response
text = response.text()

# Log to database manually
db = sqlite_utils.Database(llm.user_dir() / "logs.db")
response.log_to_db(db)
```
