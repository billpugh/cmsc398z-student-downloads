from word_grid import WordGrid

def main():
    # Read lines from standard input until a blank line
    grid_lines = []
    while True:
        line = input().strip()
        if line == "":
            break
        grid_lines.append(line)

    # Create the word grid
    word_grid = WordGrid(grid_lines)

    # Read words and search for them in the grid
    try:
        while True:
            word = input().strip()
            if word == "":
                continue
            results = word_grid.find(word)
            if not results:
                print(f"{word} not found")
            else:
                for row, col, direction in results:
                    print(f"{word} found {direction.name} from ({row},{col})")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
