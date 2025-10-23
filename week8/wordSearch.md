# Getting set up in Claude

## Initial steps

If you haven't already done these steps, do them now:

Open [Claude.ai](https://claude.ai) and log in to verify your account works.

[Download and install](https://docs.claude.com/en/docs/claude-code/setup) the CLI (command line interface) for Claude Code

## Simple Greenfield development - wordSearch

Open a terminal, change directory to week8/wordSearch, and start Claude by giving the command 'claude'.

Claude should be able to accomplish all of these steps in a few minutes.

Give the command '/init' to have it read the files in the directory and produce [wordSearch/CLAUDE.md](wordSearch/CLAUDE.md)

Ask claude to develop a design for implementing the project in python, and put the design in design.md. You can decide what you ask it to put into the design, other than that it shouldn't include any code.

Ask it to write the code for the project and test it. Tell if that if it needs to make any changes from the initial design, it should document those changes.

Write [wordSearch/myReview.md](wordSearch/myReview.md), which is your review of the design and the code. This can just be a few sentences for each. Some things to consider in your review:

* Do you believe you understand the design and code? We're not asking for absolute certainty.
* Do you see anything where the code would do the wrong thing?
* Is there anything in the code that you think it too terse and hard to understand?
* Are there any cases where the claude is more verbose or complicated than you think necessary for this project?
  * Coding models are notorious for writing explicit code to catch and log all kinds of exceptions that are unlikely to occur, or if they occur, there is nothing to do but give up.
