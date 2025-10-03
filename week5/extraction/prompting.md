# Prompting with LLM

Let's start by running some prompts using the LLM command-line interface.

## Setting a default model

Let's switch to [gpt-5-mini](https://platform.openai.com/docs/models/gpt-5-mini) as our new default model:

```bash
llm models default gpt-5-mini
```

## Running a prompt

The LLM command-line tool takes a prompt as its first argument:

```bash
llm 'Ten pun names for a teashop run by a terrapin and a blue crab'
```

## What did that do for us?

Let's run a prompt the manual way, using `curl` and the OpenAI API:

```bash
curl https://api.openai.com/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $(llm keys get openai)" \
  -d '{
    "model": "gpt-5-mini",
    "messages": [
      {"role": "user", "content": "Ten pun names for a teashop run by a terrapin and a blue crab"}
    ]
  }'
```
Now try that again with `"stream": true` to see what the streaming response looks like:

```bash
curl https://api.openai.com/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $(llm keys get openai)" \
  -d '{
    "model": "gpt-4.1-mini",
    "stream": true,
    "messages": [
      {"role": "user", "content": "Ten pun names for a teashop run by a terrapin and a blue crab"}
    ]
  }'
```

Every API provider has a similar, albeit slightly different, way of doing this. LLM and its plugins provide wrappers around those APIs so you don't need to think about those differences.

## Continuing the conversation

The `llm -c` flag stands for `--continue` - it lets you continue the most previous conversation:

```bash
llm -c 'Three more with darker overtones'
```

## Seeing it in the logs

LLM logs every prompt and response to a SQLite database. You can see the location of that database by running:

```bash
llm logs path
```
The `llm logs` command shows logged conversations. Use `-c` for the most recent conversation:

```bash
llm logs -c
```
The output looks something like this:
```
# 2025-10-02T15:13:24    conversation: 01k6jqrwpht0azk2831x2w8te0 id: 01k6jqrd0xramf70v1fxkt613k

Model: **gpt-5-mini**

## Prompt

Ten pun names for a teashop run by a terrapin and a blue crab

## Response

1. Shell & Steep
2. Claw & Cup Tea Co.
3. The Steeping Shell
...

```
As you can see, the output is in Markdown format. I frequently share my conversation logs by pasting that into a [GitHub Gist](https://gist.github.com).

Add the `-u` (short for `--usage`) flag to see how many tokens were used in the conversation:

```bash
llm logs -c -u
```

You can also get output in JSON using the `--json` flag:

```bash
llm logs -c --json
```
Every conversation has an ID. If you know the ID of a conversation you can retrieve its logs using `--cid ID`.

```bash
llm logs --cid 01k6jqrd0xramf70v1fxkt613k
```
The `-s` option stands for `--short` and provides a more compact view, useful for finding conversation IDs:

```bash
llm logs -s
```
Add `-q` to search:

```bash
llm logs -s -q 'terrapin'
```
And `-n 0` to see **every** match:

```bash
llm logs -s -q 'terrapin' -n 0
```

## Browsing the logs with Datasette

[Datasette](https://datasette.io/) is my open source tool for exploring SQLite databases. Since LLM logs to SQLite you can explore that database in your web browser using Datasette like this:

```bash
datasette "$(llm logs path)"
```
This will start a local web server which you can visit at `https://localhost:8001/`

## Using different models

Use the `-m` option to specify a different model. You can see a list of available models by running:

```bash
llm models list
```
Add the `--options` flag to learn more about them, including what options they support and what capabilities they hav:
```bash
llm models list --options
```
Let's get some pun names for a teashop from the weaker model  `gpt-5-nano`:

```bash
llm '"Ten pun names for a teashop run by a terrapin and a blue crab"' -m gpt-5-nano
```

### Logs are shared across llm installations

If you have multiple projects where you are using the llm tool, by default they all share the same user directory, which is where keys and logs are stored. This makes things simpler, but can also be surprising if you had intended that a project have its own set of keys and log files. Typically, the user directory is:

- **macOS**: `~/Library/Application Support/io.datasette.llm/`
- **Linux**: `~/.config/io.datasette.llm/`
- **Windows**: Varies based on system

The command `llm logs path` will tell you the current log file path, which will be located inside the user directory.

You can customize this location using the `LLM_USER_PATH` environment variable:

```bash
export LLM_USER_PATH=/path/to/my/custom/directory
```

## Piping in content

The best thing about having a command-line tool for interacting with models is you can pipe things in!

## Using system prompts

A **system prompt** is a special kind of prompt that has higher weight than the rest of the prompt. It's useful for providing instructions about *what to do* with the rest of the input.
```bash
cat pyproject.toml | llm -s 'describe the libraries used by this python project'
```

## Prompting with an image

LLM supports **attachments**, which are files that you can attach to a prompt. Attachments can be specified as filepaths or as URLs.

Let's describe a photograph:

```bash
llm -a https://www.cs.umd.edu/class/fall2025/cmsc398z/files/week5a.jpg 'Describe this image' -u
```
That `-u` causes the token usage to be displayed. You can paste that token line into https://www.llm-prices.com/ and select the model to get a price estimate.

## Using fragments

The `-f` option can be used to specify a **fragment** - an extra snippet of text to be added to the prompt. Like attachments, these can be filepaths or URLs.

Fragments are mainly useful as a storage optimization: the same fragment will be stored just once in the database no matter how many prompts you use it with.

Here's our `requirements.txt` example again, this time with a fragment:

```bash
llm -f pyproject.toml 'describe the libraries used by this python project'
```
The `-e` option can be used with `llm logs` to expand any fragments:

```bash
llm logs -c -e
```

## Fragment plugins

The most exciting thing about fragments is that they can be customized with **plugins**.

Install the [llm-fragments-github](https://github.com/simonw/llm-fragments-github) plugin like this:

```bash
llm install llm-fragments-github
```
This adds several new fragment types, including `github:` which can be used to fetch the full contents of a repository and `issue:` which can load an issue thread.

```bash
llm -f issue:https://github.com/simonw/llm/issues/898 -s 'summarize this issue'
```
Or let's suggest some new features for that plugin:

```bash
llm -f github:simonw/llm-fragments-github -s 'Suggest new features for this plugin' -u
```

This is a good point for a digression to talk about **long context** and why it's such an important trend.

