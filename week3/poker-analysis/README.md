# Poker analysis project

Your task with this project is to examine a set of 7 playing cards, and determine the best poker
that can be made from it.

The different kinds of poker hands are define by the enum HankRank defined in hand_rank.py.

There are several levels to completing this project, and two side quests. The custom instructions for
coaching mode are not present in this folder, and neither is the setting to disable auto-complete.

If you already have access to another coding model (e.g., cursor, Claude Code, OpenAI codex), you are welcome to use it for this project.

## What you need to update and submit

* `Notes.md` Update this with notes about your work on the project. If you run out of time to complete this during class, you can submit it later. This file is in lieu of submitting a Google form for in class work this week.  

* `Design.md` If you created any design documentations for the project, either by yourself or with the help of AI, put that documentation in this file.

* `poker_analysis.py` Update this with the code you need to analyze a poker hand. You may create additional python files to hold your code if you wish.

* `test_harness.py` Update this to call the appropriate methods in poker_analysis.py

* `main.py` If you wish to have python script you can use to manually invoke your code, put it in main.py. If you wish (see side-quests), you can write code so that if you give it less than 7 cards, it runs many simulations of how the remaining cards could be dealt, and gives you a percentile breakdown of the chance of getting various hands. This code will not be tested.

* `chat.md` Copy and paste your chat dialog into chat.md

You should not modify `hand_rank.py` or `test_poker_hand.py`.

## Card representation

Cards are represented by a two letter string, the first of which is one of A23456789TJQK, and the second of which is one of SHDC. You don't have to consider the situation of duplicate cards in a hand, or invalid cards.

## Achievement levels and test data

There are test cases to handle each of the following 3 levels and each of the kinds of poker hands in the testData directory.  Each file consists of several test cases, consisting of 7 cards, and the
5 cards that should be returned for that. Note that suit doesn't matter in comparing cards, you can substitute different cards of the same rank.

The file test_poker_hand.py contains unit tests that use the data files to check all of the levels of functionality described below. You can run the all of the tests using

```shell
uv run python -m unittest test_poker_hand
```

## Unit tests

The tests in test_poker_hand.py call a method get_best_hand(cards) defined in test_harness.py. There is code similar to that
function in my code, but it more information than get_best_hand does. Rather than forcing you to match what my function did,
you just need to change get_best_hand(cards) to call whatever methods in your code it needs, extract the required information
and return it.

### Level 1

Given a list of seven cards, determine the HandRank of the best hand that can be made from it.

### Level 2

Given a list of seven cards, determine the HandRank of the best hand that can be made from it and the cards that count towards it. For example, if the 7 cards contain one pair, you only need to identify the cards that make up the pair.

### Level 3

Given a list of seven cards, determine the HandRank of the best hand that can be made from it
and which 5 cards are in it, listed in the order that should be used to compare to hands of the same
HandRank to determine which one is better. For example, for the cards 3S 6S 3D 5C QC QD AH, the 5 cards
used for two pairs is QC QD 3S 3D AH, in the following order:

* The highest rank pair
* The lowest rank pair
* The kicker (an Ace in this case)

## Side quests

THe following are projects you might enjoy, but will not be tested.

### Given a partial set of 7 cards, determine chance of final hand

Given 0-6 cards, run many trials, dealing out additional cards to get to 7 cards and then seeing the best hand you can make with those cards. Calculate the chance of getting each hand.

You might want to allow the number of trials to be specified on the command line. In the example below I used 1,000,000 trials, which is a lot, and take a several minutes to run. Your results will not match exactly:

```text
Enter cards (e.g. 'AS 9H'), or 'stop' to quit.
> AS 9H
           hand  percent  trials  
            All:  100.0% 1000000  
      HIGH_CARD:   19.7%  197251   
       ONE_PAIR:   46.0%  460427 
       TWO_PAIR:   22.8%  227625 
THREE_OF_A_KIND:    4.5%   44719  
       STRAIGHT:    2.7%   26719   
          FLUSH:    2.0%   19655   
     FULL_HOUSE:    2.2%   22129  
 FOUR_OF_A_KIND:    0.1%    1307  
 STRAIGHT_FLUSH:    0.0%     145   
    ROYAL_FLUSH:    0.0%      23 
```

### Given a partial set of 7 cards, determine the chance of winning or splitting the pot

Given 0-7 cards, treat the first two (if any) as the user's hole cards, and the remaining cards as community cards. Run a bunch of trials, and determine the chance that the user's hand would beat or tie the best hand of a group of other players (using the same community cards).

In order to do this, you will need to implement functionality to determine,
for example, if two hands both have a three of a kind, if one hard is stronger than the other.

Note: I came up with something clever so that you don't have to do a completely separate trial for
each number of players. There are less clever ways to do it that might have been fast enough, but I like
elegant and clever coding. Might have been better to also do a more brute force approach and compare them.

You might want to allow the number of trials to be specified on the command line. In the example below I used 1,000,000 trials, which is a lot, and take a several minutes to run. Your results will not match exactly:

```text
Enter cards (e.g. 'AS 9H'), or 'stop' to quit.
> AS 9H
           hand  percent  trials    2      3      4      5      6      7      8      9     10
            All:  100.0% 1000000   62.1   43.3   32.8   26.3   21.9   18.7   16.3   14.3   12.7
      HIGH_CARD:   19.7%  197251   32.1   10.1    3.0    0.9    0.2    0.1    0.0    0.0    0.0
       ONE_PAIR:   46.0%  460427   59.3   37.3   25.0   17.7   13.1   10.0    7.8    6.2    4.9
       TWO_PAIR:   22.8%  227625   80.2   65.2   53.5   44.3   37.0   31.2   26.4   22.6   19.4
THREE_OF_A_KIND:    4.5%   44719   82.4   70.1   61.3   54.8   49.9   46.0   42.8   40.1   37.7
       STRAIGHT:    2.7%   26719   91.9   85.0   79.1   74.1   69.7   65.8   62.5   59.5   56.9
          FLUSH:    2.0%   19655   90.6   82.6   75.7   69.8   64.8   60.5   56.8   53.6   50.9
     FULL_HOUSE:    2.2%   22129   96.7   93.6   90.7   88.1   85.6   83.3   81.1   79.1   77.3
 FOUR_OF_A_KIND:    0.1%    1307  100.0  100.0   99.9   99.9   99.9   99.9   99.9   99.9   99.8
 STRAIGHT_FLUSH:    0.0%     145   98.6   97.2   95.8   94.4   92.9   91.5   90.1   88.7   87.3
    ROYAL_FLUSH:    0.0%      23  100.0  100.0  100.0  100.0  100.0  100.0  100.0  100.0  100.0
```

