# Setup

## Setting up your environment

To setup your environment, cd to the week5 directory, and give the commands:


```bash
uv venv
uv sync
source .venv/bin/activate
```

Run this command to see if the packages installed correctly:

```bash
llm --version
```
You should see this:
```
llm, version 0.27.1
```

## Configuring the OpenAI API key

You'll need an OpenAI API key for this workshop. You can either get your own here:

[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Or you can use a shared one created for this class. You'll need the password that is distributed in class:

* [Get the workshop API key (password required)](https://tools.simonwillison.net/encrypt#zHanbpCyyYjp8EoUZAtjyakfBbuX/GszQaNoadiKi9VubDT9eLjIAei1w4f4vP+SF9UgxZ70gp4izV2YZZikz1Oz9GNfJM65sfP6omtm5/i/sDdvEzA3j6SWjx1yW+Iw1MzjIeVQk6TNTrVGpGdRKA6OuT+P3CLkWzuWxwOsL+5U5gqA9QxKS9KBANrxwfWfjO9yjNpkuVhgbOuqIZtIBqGcH2yIzT3Bunk1DSNaEGM6jWog4PKuXXm5x3lZJdps4pWoVFlnr/Y5dQfPUZETNw==)

This shared key is restricted to the following models: `gpt-5-mini`, `gpt-5-nano`.

Key obtained, you can configure it for LLM like this:

```bash
llm keys set openai
# Paste your key here
```

Set your default model to be gpt-5-mini.

```bash
llm models default gpt-5-mini
```

## Testing that it worked

Test that the keys works like this:
```bash
llm 'five fun facts about terrapins'
```
The key will be saved to a JSON file. You can see the location of that file by running:
```bash
llm keys path
```

A useful trick is that `llm keys get openai` will print the key out again. You can use this pattern to use that key with other tools that require an environment variable:

```bash
export OPENAI_API_KEY="$(llm keys get openai)"
```
