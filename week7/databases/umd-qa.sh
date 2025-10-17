#!/usr/bin/env bash
set -euo pipefail

# Question is all args joined
question="$*"
if [ -z "$question" ]; then
  echo "Usage: $0 \"Your question here\""
  exit 1
fi

# Choose a wrapper that forces unbuffered / pty output for streaming if available
if command -v stdbuf >/dev/null 2>&1; then
  wrapper_cmd=(stdbuf -o0 -e0)
elif command -v unbuffer >/dev/null 2>&1; then
  wrapper_cmd=(unbuffer)
elif command -v script >/dev/null 2>&1; then
  # script provides a pty and typically causes streaming output
  wrapper_cmd=(script -q /dev/null --)
else
  wrapper_cmd=()
fi

# Run the pipeline: search -> llm answer (with wrapper if available)
if [ ${#wrapper_cmd[@]} -gt 0 ]; then
  llm similar -c "$question" -d course_embeddings.db courses \
    | "${wrapper_cmd[@]}" llm -s "Answer the question: $question" -m gpt-5-mini
else
  echo "Warning: no stdbuf/unbuffer/script found; output may be buffered. Install coreutils (stdbuf) or expect (unbuffer) for better streaming." >&2
  llm similar -c "$question" -d course_embeddings.db courses \
    | llm -s "Answer the question: $question" -m gpt-5-mini
fi
