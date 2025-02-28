import csv
import sys

from poem_writer import extract_anchor_word_positions, read_input_file

def extract_anchor_word_positions_non_spacy(input_text, anchor_word):
    """
    Finds all occurrences of the anchor word in the corpus and returns their positions.
    
    :param corpus_text: A string containing the input text (corpus).
    :param anchor_word: A string representing the word to search for (e.g., "you").
    :return: A list of indices where the anchor word occurs.
    """
    input_words = input_text.split()
    return [i for i, token in enumerate(input_words) if token.lower() == anchor_word.lower()]

def print_current_poem(poem, current_line):
    """Prints current poem, line by line"""
    print("\nCurrent poem\n----------\n")
    for line in poem:
        print(line)
    print(f"{' '.join(current_line)} ...")  # Show the new line so far
    print("----------")

def construct_poem_interactive(table_data):
    poem = []  # Holds the lines of the poem
    current_line = []  # Holds the current line being built
    end_poem = False
    
    for i, row in enumerate(table_data):
        if end_poem: break
        print_current_poem(poem, current_line)

        # Display words with indices on a single line
        print(f"Options: ", end="")
        print(", ".join([f"{idx+1}: {word}" for idx, word in enumerate(row[1:])]))

        # Get user's choice of word
        while True:
            user_choice = input("Choose a word by typing the corresponding number \
                                \n(or type 'n' to start a new line, or 'x' to end the poem): ")
            if user_choice.lower() in ["n", "x"]:
                # Start a new line
                poem.append(' '.join(current_line))
                current_line = []  # Reset current line
                if user_choice.lower() == "x":  end_poem = True
                break
            try:
                choice_idx = int(user_choice)  # Subtract 1 to match index
                if 0 <= choice_idx < len(row):
                    current_line.append(row[choice_idx])  # Add chosen word to the current line
                    break
                else:
                    print("Invalid choice. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please choose a number or type 'new line'.")
    
    # Append the last line to the poem
    poem.append(' '.join(current_line))
    
    # Write the poem to a text file
    with open("output_poem.txt", "w") as file:
        for line in poem:
            file.write(line + "\n")
    
    print("\nPoem written to 'output_poem.txt'")

def load_csv_as_list(filename):
    """Loads a CSV file and returns it as a list of lists"""
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]  # Convert each row into a list and return as a list of lists


def make_table(input_text: str, index_list: list, words_per_row=7):
    # Split the input_text into a list of words
    words = input_text.split()
    
    # Prepare a list to hold rows for the table
    table_data = []

    # Loop through the index_list
    for index in index_list:
        # Check if there are at least n words after the current index
        if index + words_per_row <= len(words):
            # Get the next n words starting from the index
            row = words[index:index + words_per_row + 1]
            table_data.append(row)
    
    # Write the table_data to a CSV file
    with open('output_table.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)

# input_text = read_input_file('../data/input_text_files/Elon-Alice.txt')
# index_list = extract_anchor_word_positions_non_spacy(input_text, anchor_word="you")

# make_table(input_text, index_list)


# Example usage
table_data = load_csv_as_list('output_table.csv')

# Start the interactive poem construction
construct_poem_interactive(table_data)
