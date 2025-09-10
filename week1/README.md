# CMSC 398Z - Week 1 - Sept 5th, 2025

## Slides

* [Slides from lecture](slides.pdf)

## Getting your computer set up

* For MacOS users, install xcodetools
    * You may already have this installed.  Try entering `xcode-select --version`
    into the terminal
    * If you don't have it installed, type `xcode-select --install` into the terminal

* For Windows users, install Windows Subsystem for Linux (WSL 2)
    * See [discussion](https://g.co/gemini/share/d677a8cc6b9d) with Gemini
    * [Install WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
    * [Install Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/install)
    * Once you have VSCode installed, install [WSL Extension for VSCode](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)


* [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
    * `uv` and `uvz` get added to ``~/.local/bin``
    * The uv installer will give you instructions to follow if you need to add
    that directory to your path
    * Executing ``uv python install --default --preview`` will install `python`
    in `~/.local/bin`

* [Download VS Code](https://code.visualstudio.com/Download)

* [Install the Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

* [Install the Github Copilot extension for VS
Code](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)

## Python tutorials and style guides

* [Python introduction slides](https://docs.google.com/presentation/d/1tOC0EOiF4Dkavjz3To07wXC_EdKW32qvZyN3XizvMlo/edit?slide=id.p1#slide=id.p1)
from [Dr. Fardina Alam's](https://www.fardinafathmiulalam.com) [Spring 2024 CMSC320](https://cmsc320.github.io)
* [Harvard's CS 50 course](https://cs50.harvard.edu/python/)
* [Official Python Style guide](https://peps.python.org/pep-0008/)
* [Google's Python style guide](https://google.github.io/styleguide/pyguide.html)

## Coding projects

### completed instructor project - [Word Search in a Grid](wordSearch)
### Project 1a - [Playing wordle](playWordle)

* Clone git repository containing project starter files [https://github.com/billpugh/cmsc398z-student-downloads](https://github.com/billpugh/cmsc398z-student-downloads)
* cd to that directory
* open week1/playWordle in VSCode, work on project
* Save your chat transcript at chat.md
* Submit your Python code and chat.md to the [submit server](https://submit.cs.umd.edu/)
    * You can either use `java -jar submit.jar` in the project directory, or
    just upload playWordle.py and chat.md to the submit server

## Learning logs

* [Questions on class work and projects, due noon Tuesday, Sept 9th](https://forms.gle/F4z6GPH6Rso4p93y5) 
* [Questions on readings, log due noon Friday, Sept 12th](https://forms.gle/GCX2wAdP7UxswYHU6)

## Readings for Friday, Sept 12th

* NYTimes [How Do You Teach Computer Science in the A.I. Era?](https://www.nytimes.com/2025/06/30/business/computer-science-education-ai.html?unlocked_article_code=1.S08.mSBd.EL5BZbNtgtpE&smid=url-share)
* The Fly Blog - [My AI Skeptic Friends Are All Nuts](https://fly.io/blog/youre-all-nuts/)
* Harper Reed - [An LLM Codegen Hero's Journey](https://harper.blog/2025/04/17/an-llm-codegen-heros-journey/)
* optional: [How AI Coding Agents Will Change Your
    Job](https://youtu.be/TECDj4JUx7o?si=QX0wba-dXTQ7VbxV) from Y Combinator
