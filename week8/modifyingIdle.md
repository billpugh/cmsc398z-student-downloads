# Modifying the IDLE editor

For this project, we are going to use a project from UCSD's [Spring 2025 offering of CSE 190](https://cse190largecodebases.github.io/sp25/).

In particular, we are going to ask you to modify the IDLE editor distributed as part of cpython. This is part of [Project 1](https://cse190largecodebases.github.io/sp25/projects/idle-dev-environment) and [Project 2](https://cse190largecodebases.github.io/sp25/projects/go-to-line-feature) of the UCSD course.

* Try running idle. You may already have it on your path as 'idle3', or you can use 'uvx python -m idlelib'

* Clone the [cpython repository from GitHub](https://github.com/python/cpython) - You can do this within the week8 directory, or someplace else. 
  * You won't be submitting this directory as part of your project submission this week. Instead, after you are done you will copy some files to the week 8 directory to submit. 
* If you want to be able to actually build and test the code, you will need to [install the dependencies](https://devguide.python.org/getting-started/setup-building/#install-dependencies). If this is challenging for you to do, you can skip this and just ask Claude to build the code without being able to test it.
* move the [cpython-CLAUDE.md](cpython-CLAUDE.md) file into the cpython directory and name it 'CLAUDE.md' This is what I got giving the '/init' command inside the cpython directory. You could do that yourself rather than moving this file, but this will save you a minute or two of type and the Claude usage needed to build it. Note that using '/init', like any LLM use, is nondeterministic. I tried using it twice, and got different files, one longer than the other
* Tell Claude that we are only going to be making changes to '@Lib/idlelib'.
* Read the [Project 2 instructions](https://cse190largecodebases.github.io/sp25/projects/go-to-line-feature) about changing the Goto Line feature in IDLE.
* Ask Claude to create a 'goto-design.md' file describing the the design of the code changes needed to implement required features from the CSE 190 Project 2 description. You might have a dialog with Claude about how those features should work or how to implement those features, any reasonable choice is fine.
* Look at the 'goto-design.md' file, ask Claude if there is any choices that look questionable.
* Ask Claude to implement and write tests for the new Goto Line feature.
* Ask Claude to run the tests and iterate if they aren't all working.
* Ask Claude to run the editor so you can examine the new functionality yourself.
* Ask Claude to create a 'goto-implementation.md' file that describes the changes to the functionality (but not the test cases), including the changed code.
* Create a file 'goto-review.md' that describes your experiences working with Claude on this project and what you think if the the contents of 'goto-design.md' and  'goto-implementation.md'
* Copy all three of the goto-*.md files to the week8 directory. You will be submitting those for your work this week.
