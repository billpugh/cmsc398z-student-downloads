import argparse
import random
from collections import deque, Counter
from termcolor import colored


class MarkovModel:
    def __init__(self, n):
        self.n = n
        self.predictions = {}
        self.reset()

    def reset(self):
        self.prev = deque([None] * self.n, maxlen=self.n)

    def saw(self, word):
        key = tuple(self.prev)
        if key not in self.predictions:
            self.predictions[key] = [word]
        else:
            self.predictions[key].append(word)
        self.prev.append(word)

    def learn_from(self, filename):
        self.reset()
        last_empty = False
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.isupper():
                    self.reset()
                    last_empty = False
                    continue
                if line:
                    words = line.split()
                    for word in words:
                        self.saw(word)
                    last_empty = False
                else:
                    if not last_empty:
                        self.saw('\n')
                    last_empty = True
        self.saw(None)

    def predict(self):
        key = tuple(self.prev)
        options = self.predictions.get(key)
        if not options:
            return None, 0.0
        next_word = random.choice(options)
        self.prev.append(next_word)
        return next_word, entropy(options)


def entropy(words):
    total = len(words)
    if total == 0:
        return 0.0
    counts = Counter(words)
    sum_sq = sum(count ** 2 for count in counts.values())
    return 1 - (sum_sq / (total * total))


def main():
    parser = argparse.ArgumentParser(description="Markov text model")
    parser.add_argument('-n', type=int, default=2,
                        help='Order of the Markov model')
    parser.add_argument('-l', action='store_true', help='light mode')
    parser.add_argument('files', nargs='+', help='Text files to learn from')
    args = parser.parse_args()

    model = MarkovModel(args.n)
    for fname in args.files:
        model.learn_from(fname)

    model.reset()
    line_length = 0
    while True:
        word, entropy_score = model.predict()
        if word is None:
            break
        if word == '\n':
            if line_length > 0:
                print()
            print()
            line_length = 0
            continue
        if line_length + len(word) + 1 > 80:
            print()
            line_length = 0
        color = 255
        if entropy_score > 0.1:
            color = 200 - 150*entropy_score
        if args.l:
            text_color = (255-color, 0, 0)
        else:
            text_color = (255, color, color)
        print(colored(word, text_color), end=' ')
        line_length += len(word) + 1


if __name__ == "__main__":
    main()
