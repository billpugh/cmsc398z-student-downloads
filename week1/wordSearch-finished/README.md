# Word Search

The goal of this project is to take a rectangular grid of letters, and then a list of words, and look for those words in the grid. Words can be found in the grid in any of 4 orientations (up, down, left or right)

For each word, say whether it doesn't exist in the grid, or give the starting location and direction for the word in the grid.

Each letter in the grid can be used for multiple words.

## Sample data (provided in input1.txt)

### Grid

```text
RMELLLGILAZK
BFWHFMOZGLZT
BDTUCNDSLSHA
YYOFUNCTIONC
FAHSILTASKOС
HNHJOHELLOTA
YFMPIPWLBTEJ
LGODNEZYZZIT
```

### Words (partial list)

```text
CAT
DOG
FUNCTION
```

## Input file format

The program should read from standard input (although the ability to read from a file specified on the command line would be nice).

The word grid is described by a series of lines, all of the same length, terminated by an empty line. You can assume all the characters are upper case letters.

After the empty line, each line will contain one word. You can assume it is all upper case letters.

If a word occurs multiple times, you may optionally list all occurrences.

For today, you only need to consider words oriented up, down, left and right. Diagonal orientations might be be added as a feature, design your system to anticipate that.
