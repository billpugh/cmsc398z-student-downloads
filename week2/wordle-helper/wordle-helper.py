def main():
    """
    Main loop for Wordle helper. Handles '?', '??', '!', and guess/analysis input.
    """
    wordle_file = "wordleWords.txt"
    original_words = read_wordle_words(wordle_file)
    words = original_words[:]

    print(f"{len(words)} words loaded.")


if __name__ == "__main__":
    main()



