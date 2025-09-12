# Documenting Markov Model text generation

This project takes training files on the command line, and then generates random text based on the training data. The text is colored to show you where the model had a choice in what word came next. If a word is white or black, there was only one choice. For red words, there was a choice. The more intense the red color, the more choices. 

For this project, the [code is completely written](markov_model.py), but undocumented. Your task is to spend time trying to understand this code and add appropriate comments. In particular, you need to add [docstring](https://peps.python.org/pep-0257/) comments for:

* The class MarkovModel
* Every function

And comment the following, even if they aren't technically docstrings:

* Every field/attribute of MarkovModel
* Any if statement where the purpose of the if statement isn't clear from context. There is at least one such if statement, and you will likely need to use the debugger to run the code and have a breakpoint when the loop body is executed to understand it.

## running the project

You will need to use `uv venv` to build the uv venv in order to be able to run the project.
Typing ``uv run markovModel Sherlock.txt` will generate text from the stories of Sherlock Holmes. 
Examine the code to understand what can be supplied on the command line.

## References on Markov Text generation

* Description of Markov text generation and a python program to do it <https://benhoyt.com/writings/markov-chain/>
* [Mark Shaney](https://en.wikipedia.org/wiki/Mark_V._Shaney) - some interesting usenet history