# Wordle helper

Write a python program designed to help you when you are playing wordle.
You are welcome/encouraged to adapt code you wrote for playing wordle. 

You can use the words in wordleWords.txt as the list of possible Wordle words. Once the NY Times 
took over Wordle, they have been adding words to the list of feasible words, and there is no
reliable or definitive list (that I have found) of the current wordle words.

You start by entering the words you have chosen and what colors they were marked. At each step, it will tell you how many words remain.

There are three commands you can implement, of increasing difficulty:

* ? - show 10 of the remaining words. Ideally, randomly select 10 to show if there are more than 10
* ? *letters* - show 10 of the remaining words that each contain all of the letters specified
* ?? - Recommend which words to pick. List up to 10, with strongest recommendation last.

## Example

The following is an example of my program running. You do not need to exactly match the textual output of my code.

```text
2337 words loaded.
Enter ? letters for feasible words, ?? for guidance, ! to reset, or guess and analysis
Enter command: clasp bbbbb
472 words remain.
Enter command: ?
472 matching words found. Showing 10:
BEING
BRIEF
ENVOY
GENRE
HYMEN
MURKY
QUOTH
THEIR
THIRD
UNDER
Enter command: ? er
147 matching words found. Showing 10:
DINER
FIBRE
FOYER
GENRE
GORGE
GREEN
JERKY
MOWER
NERDY
OUTER
Enter command: ??
Recommended words, strongest recommendation last
TREND
DINER
FORTE
TIGER
GONER
INTER
ROUTE
DRONE
TRIED
TENOR
Enter command: 
```

