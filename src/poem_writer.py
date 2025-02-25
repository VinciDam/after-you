import argparse
import os
import spacy

# Load the spaCy model for POS tagging
nlp = spacy.load("en_core_web_sm")

def pos_tag_poem(poem_text):
    """
    Tokenizes the poem and returns a list of (word, POS) tuples.
    
    :param poem_text: A string containing the poem.
    :return: A list of tuples, each containing (word, POS tag).
    """
    doc = nlp(poem_text)
    return [(token.text, token.pos_) for token in doc if token.pos_ not in 
            ['PUNCT', 'SPACE', 'EOL']] # exclude certain POS

def extract_anchor_word_positions(corpus_text, anchor_word):
    """
    Finds all occurrences of the anchor word in the corpus and returns their positions.
    
    :param corpus_text: A string containing the input text (corpus).
    :param anchor_word: A string representing the word to search for (e.g., "you").
    :return: A list of indices where the anchor word occurs.
    """
    doc = nlp(corpus_text)
    return [i for i, token in enumerate(doc) if token.text.lower() == anchor_word.lower()]

def find_matching_pos_word(corpus_words, current_pos, target_pos_tag):
    """
    Finds the first word in the corpus that matches the target POS tag.
    
    :param corpus_words: A list of tuples [(word, POS tag)] from the corpus.
    :param current_pos: The current position in the corpus (starting point for search).
    :param target_pos_tag: The POS tag to search for.
    :return: A tuple (word, new_position) or "<WORD-NOT-FOUND>" if no match is found.
    """
    total_words = len(corpus_words)
    
    # Start searching from the current position
    for i in range(current_pos + 1, total_words + current_pos + 1):  # Allow for cycling
        i_mod = i % total_words  # Ensure the index wraps around
        word, pos_tag = corpus_words[i_mod]
        
        if pos_tag == target_pos_tag:
            return word, i_mod  # Found a match, return the word and new position
    
    return "<WORD-NOT-FOUND>", i_mod

def generate_poem(input_text, input_poem, anchor_word="you"):
    """
    Generates a new poem based on the structure and POS tags of the input poem.
    
    :param input_text: A string containing the corpus text.
    :param input_poem: A string containing the original poem.
    :param anchor_word: A string representing the word to search for (e.g., "you").
    :return: A string representing the generated poem with the same structure as input_poem.
    """
    
    # Step 1: Tokenize the input poem and get POS tags
    tagged_poem = pos_tag_poem(input_poem)
    
    # Step 2: Tokenize the corpus text for later use
    corpus_words = nlp(input_text)
    
    # Step 3: Extract the positions of the anchor word in the corpus
    anchor_word_positions = extract_anchor_word_positions(input_text, anchor_word)
    
    # Step 4: Prepare to generate the new word sequence
    word_sequence = []
    current_anchor_position_index = 0
    
    # Step 5: Iterate over the tagged poem, find matching words for each POS
    for word, target_pos_tag in tagged_poem:
        # Get the current anchor word's position
        current_anchor_position = anchor_word_positions[current_anchor_position_index]
        
        # Find the matching word from the corpus using find_matching_pos_word
        matching_word, new_position = find_matching_pos_word(
            corpus_words=[(token.text, token.pos_) for token in corpus_words],  # tokenize corpus
            current_pos=current_anchor_position, 
            target_pos_tag=target_pos_tag
        )
        
        # Append the found word to the word sequence
        word_sequence.append(matching_word)
        
        # Move to the next anchor word position for the next match
        current_anchor_position_index = (current_anchor_position_index + 1) % len(anchor_word_positions)
    
    # Step 6: Format the output poem with the word sequence and the original poem structure
    poem_structure = [len(line.split()) for line in input_poem.splitlines()]
    formatted_poem = format_output_poem(word_sequence, poem_structure)
    
    return formatted_poem

def format_output_poem(word_sequence, poem_structure):
    """
    Formats the word sequence into the same structure as the input poem.
    
    :param word_sequence: A list of words to format.
    :param poem_structure: A list of integers representing the number of words per line.
    :return: A string representing the formatted poem.
    """
    poem_lines = []
    word_index = 0
    
    # For each line in the input poem, grab the corresponding number of words
    for words_in_line in poem_structure:
        line = ' '.join(word_sequence[word_index: word_index + words_in_line])
        poem_lines.append(line)
        word_index += words_in_line
    
    return '\n'.join(poem_lines)

def read_input_file(file_path):
    """
    Reads a text file and returns its content as a string.
    
    :param file_path: A string containing the path to the file.
    :return: A string with the file content.
    """
    with open(file_path, 'r') as file:
        return file.read()  # Return the content as a single string

def write_poem_to_file(poem, output_file_path):
    """Write the generated poem to a file."""
    with open(output_file_path, 'w') as f:
        f.write(poem)

def create_file_name(input_text_file, input_poem):
    """Name output file according to input poem + text."""
    w1 = os.path.basename(input_text_file).split('.')[0]
    w2 = os.path.basename(input_poem).split('.')[0]
    return f"{w1}-{w2}.txt"

def main(input_text_file, input_poem, anchor_word):

    output_file = create_file_name(input_text_file, input_poem)
    output_file = os.path.join('../data/output_poems', output_file)

    # Read the input files
    input_text_content = read_input_file(input_text_file)
    input_poem_content = read_input_file(input_poem)

    # Generate the poem based on the input files
    generated_poem = generate_poem(input_text_content, input_poem_content, anchor_word)

    # Write the generated poem to a new file
    write_poem_to_file(generated_poem, output_file)

    print("Poem generation complete. Check the 'generated_poem.txt' file.")

if __name__ == "__main__":

    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Build a poem.")
    
    # Define expected arguments: two files and a string
    parser.add_argument('input_text', type=str, help='Path to the input text (e.g. interview)')
    parser.add_argument('input_poem', type=str, help='Path to the input poem. The structure and \
                        POS of this poem will be mapped to the output poem')
    parser.add_argument('--anchor_word', type=str, default="you", help='The POS following the \
                        anchor word will be used.')
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.input_text, args.input_poem, args.anchor_word)