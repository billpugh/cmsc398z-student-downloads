import unittest
import os
from collections import Counter
from hand_rank import HandRank

from test_harness import get_best_hand

def ranks(cards):
    return [card[0] for card in cards]

def all_in(cards, possible):
    return all(card in possible for card in cards)

def main_cards_count(rank):
    """
    Returns the number of non-kicker cards that make up the given HandRank.
    For HIGH_CARD: 0, ONE_PAIR: 2, TWO_PAIR: 4, THREE_OF_A_KIND: 3, STRAIGHT: 5, FLUSH: 5, FULL_HOUSE: 5, FOUR_OF_A_KIND: 4, STRAIGHT_FLUSH: 5, ROYAL_FLUSH: 5
    """
    if rank == HandRank.HIGH_CARD:
        return 0
    elif rank == HandRank.ONE_PAIR:
        return 2
    elif rank == HandRank.TWO_PAIR:
        return 4
    elif rank == HandRank.THREE_OF_A_KIND:
        return 3
    elif rank == HandRank.FOUR_OF_A_KIND:
        return 4
    else:
        return 5


class CheckRank(unittest.TestCase):
    def check_test_data_for_rank(self, rank, fileName = None):
        """
        Utility function to check that each line in testData/{rank}.txt returns the expected HandRank.
        """

        filename = os.path.join("testData", f"{fileName or rank.name}.txt")
        if not os.path.exists(filename):
            self.fail(f"File {filename} does not exist.")
        with open(filename) as f:
            for line in f:
                cards = line.strip().split()
                result = get_best_hand(cards[:7])
                self.assertEqual(result[0], rank, f"Cards: {cards} returned {result[0]}, expected {rank}")

    def test_high_card(self):
        self.check_test_data_for_rank(HandRank.HIGH_CARD)

    def test_one_pair(self):
        self.check_test_data_for_rank(HandRank.ONE_PAIR)

    def test_two_pair(self):
        self.check_test_data_for_rank(HandRank.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.check_test_data_for_rank(HandRank.THREE_OF_A_KIND)

    def test_straight(self):
        self.check_test_data_for_rank(HandRank.STRAIGHT)

    def test_wheel_straight(self):
        self.check_test_data_for_rank(HandRank.STRAIGHT, "WHEEL_STRAIGHT")

    def test_flush(self):
        self.check_test_data_for_rank(HandRank.FLUSH)

    def test_full_house(self):
        self.check_test_data_for_rank(HandRank.FULL_HOUSE)

    def test_four_of_a_kind(self):
        self.check_test_data_for_rank(HandRank.FOUR_OF_A_KIND)

    def test_straight_flush(self):
        self.check_test_data_for_rank(HandRank.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        self.check_test_data_for_rank(HandRank.ROYAL_FLUSH)

class CheckCards(unittest.TestCase):
    def check_test_data_for_cards(self, rank, fileName = None):
        """
        Utility function to check that each line in testData/{rank}.txt returns the expected HandRank,
        and that the cards in result[1] match the input cards (order may differ).
        If get_best_hand returns None for the cards, fail once for all cases.
        """
        filename = os.path.join("testData", f"{fileName or rank.name}.txt")
        if not os.path.exists(filename):
            self.fail(f"File {filename} does not exist.")
        with open(filename) as f:
            for line in f:
                cards = line.strip().split()
                result = get_best_hand(cards[:7])
                self.assertEqual(result[0], rank, f"Cards: {cards} returned {result[0]}, expected {rank}")
                # If student code returns None for cards, fail once with a clear message
                if result[1] is None:
                    self.fail(f"get_best_hand did not return cards for input: {cards[:7]}")
                self.assertTrue(all_in(result[1], cards[:7]), f"Returned cards not all in input: {result[1]} vs {cards[:7]}")
                self.assertEqual(len(result[1]), 5, f"Expected 5 cards in returned hand, got {len(result[1])}: {result[1]}")
                main_cards = main_cards_count(result[0])
                expected_ranks = Counter(ranks(cards[7:])[:main_cards])
                returned_ranks = Counter(ranks(result[1])[:main_cards])
                self.assertEqual(returned_ranks, expected_ranks, f"Ranks of cards mismatch: got {result[1]} vs {cards[:7]} expected")
                
    def test_high_card(self):
        self.check_test_data_for_cards(HandRank.HIGH_CARD)

    def test_one_pair(self):
        self.check_test_data_for_cards(HandRank.ONE_PAIR)

    def test_two_pair(self):
        self.check_test_data_for_cards(HandRank.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.THREE_OF_A_KIND)

    def test_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT)

    def test_wheel_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT, "WHEEL_STRAIGHT")

    def test_flush(self):
        self.check_test_data_for_cards(HandRank.FLUSH)

    def test_full_house(self):
        self.check_test_data_for_cards(HandRank.FULL_HOUSE)

    def test_four_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.FOUR_OF_A_KIND)

    def test_straight_flush(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        self.check_test_data_for_cards(HandRank.ROYAL_FLUSH)
                
class CheckBestCards(unittest.TestCase):
    def check_test_data_for_cards(self, rank, fileName = None):
        """
        Utility function to check that each line in testData/{rank}.txt returns the expected HandRank,
        and that the cards in result[1] match the input cards (order may differ).
        If get_best_hand returns None for the cards, fail once for all cases.
        """
        filename = os.path.join("testData", f"{fileName or rank.name}.txt")
        if not os.path.exists(filename):
            self.fail(f"File {filename} does not exist.")
        with open(filename) as f:
            for line in f:
                cards = line.strip().split()
                result = get_best_hand(cards[:7])
                self.assertEqual(result[0], rank, f"Cards: {cards} returned {result[0]}, expected {rank}")
                # If student code returns None for cards, fail once with a clear message
                if result[1] is None:
                    self.fail(f"get_best_hand did not return cards for input: {cards[:7]}")
                self.assertEqual(len(result[1]), 5, f"Expected 5 cards in returned hand, got {len(result[1])}: {result[1]}")
                self.assertTrue(all_in(result[1], cards[:7]), f"Returned cards not all in input: {result[1]} vs {cards[:7]}")

                expected_ranks = ranks(cards[7:])
                returned_ranks = ranks(result[1])
                self.assertEqual(returned_ranks, expected_ranks, f"Best cards ranks mismatch")
                
    def test_high_card(self):
        self.check_test_data_for_cards(HandRank.HIGH_CARD)

    def test_one_pair(self):
        self.check_test_data_for_cards(HandRank.ONE_PAIR)

    def test_two_pair(self):
        self.check_test_data_for_cards(HandRank.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.THREE_OF_A_KIND)

    def test_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT)

    def test_wheel_straight(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT, "WHEEL_STRAIGHT")

    def test_flush(self):
        self.check_test_data_for_cards(HandRank.FLUSH)

    def test_full_house(self):
        self.check_test_data_for_cards(HandRank.FULL_HOUSE)

    def test_four_of_a_kind(self):
        self.check_test_data_for_cards(HandRank.FOUR_OF_A_KIND)

    def test_straight_flush(self):
        self.check_test_data_for_cards(HandRank.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        self.check_test_data_for_cards(HandRank.ROYAL_FLUSH)
                


if __name__ == '__main__':
    unittest.main()
