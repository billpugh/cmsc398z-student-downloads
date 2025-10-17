# Semantic search and RAG

This section started with [some slides and background on embeddings](https://simonwillison.net/2025/May/15/building-on-llms/#llm-tutorial-intro.015.jpeg).

One of the most popular applications of LLMs is to build "ask questions of my own documents" systems.

You do **not** need to fine-tune a model for this. Instead, you can use a pattern called **retrieval-augmented generation** (RAG).

The key trick to RAG is simple: try to figure out the most relevant documents for the user's question and *stuff as many of them as possible into the prompt*.

Long context models make this even more effective. "Reasoning" models may actually be *less* effective here.

## Semantic search

If somebody asks "can my pup eat brassicas", how can we ensure we pull in documents that talk about dogs eating sprouts?

One solution is to build **semantic search** on top of **vector embeddings**.

I wrote about those in [Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/).

## Generating embeddings with LLM

LLM includes [a suite of tools](https://llm.datasette.io/en/latest/embeddings/index.html) for working with embeddings, plus various plugins that add new embedding models.

We'll start with the OpenAI hosted embedding model.

```bash
llm embed -m text-embedding-3-small-512 -c "can my pup eat brassicas?"
```
This returns a 256 long vector of floats.

More useful is if we store some information first. Let's embed all the titles and descriptions of all CMSC courses:
```bash
uv run llm embed-multi courses \
  -d cmsc_course_embeddings.db \
  --attach umd umd-202508.db \
  --sql "select course_id, title, description from umd.course_info where department='CMSC'" \
  --store \
  -m text-embedding-3-small-512
```
There's a lot going on there. We're using the 512 long `text-embedding-3-small-512` model, saving embeddings to a `cmsc_course_embeddings.db` SQLite database in a `courses` collection, using the title and description for each CMSC course. and storing the titles and descriptions along with their vectors.


Confirmed with:
```bash
llm collections -d cmsc_course_embeddings.db 
```
And now we can search that collection for items similar to a term using:
```bash
llm similar -c 'artificial intelligence' -d cmsc_course_embeddings.db courses  | jq
```

Here's a SQLite database with ALL of the course descriptions, so that our class doesn't burn through my API credits with everyone embedding the same data!

[https://www.cs.umd.edu/class/fall2025/cmsc398z/files/course_embeddings.db](https://www.cs.umd.edu/class/fall2025/cmsc398z/files/course_embeddings.db) (16 MB)

## Answering questions against those course descriptions

This time we'll build a bash script:

```bash
llm '
Build me a bash script like this:

./umd-qa.sh "What courses discuss artificial intelligence?"

It should first run:

llm similar -c $question -d course_embeddings.db courses

Then it should pipe the output from that to:

llm -s "Answer the question: $question" -m gpt-5-mini

That last command should run so the output is visible as it runs.
' -x > umd-qa.sh

chmod +x umd-qa.sh
./umd-qa.sh "What do string templates look like?"
```
I [got this](umd-qa.sh).

Usage example:
./umd-qa.sh "What courses discuss artificial intelligence?"

Notes:

- The script joins all provided arguments into the question (so you can pass a multiword question without extra quoting issues).
- For the best streaming behavior, install coreutils (for stdbuf) or expect (for unbuffer). On some systems script is already available and will also work.
- Running code that an LLM has generated without first reviewing it generally a *terrible* idea!

If you want to port the above to Python you should consult the [Working with collections](https://llm.datasette.io/en/latest/embeddings/python-api.html#working-with-collections) section of LLM's Python API documentation.

## RAG does not have to use semantic search!

Many people associate RAG with embedding-based semantic search, but it's not actually a requirement for the pattern.

A lot of the most successful RAG systems out there use traditional keyword search instead. Models are very good at taking a user's question and turning it into one or more search queries.

Don't get hung up on embeddings!

## RAG is dead?

Every time a new long-context model comes out, someone will declare the death of RAG.

I think classic RAG is dead for a different reason: it turns out arming an LLM with search tools is a much better way to achieve the same goal.

Which brings us to our next topic: {ref}`tools`.