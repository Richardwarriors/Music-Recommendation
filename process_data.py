import os

def process_prompt_data(input_file_path, output_input_file_path, output_recommendations_file_path, delimiter):
    """
    Reads an input file, splits each line by a delimiter, and writes the
    parts to two separate output files. Strips whitespace from each part.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
             open(output_input_file_path, 'w', encoding='utf-8') as input_outfile, \
             open(output_recommendations_file_path, 'w', encoding='utf-8') as rec_outfile:

            for line in infile:
                parts = line.split(delimiter, 1)  # Split only on the first occurrence

                if len(parts) == 2:
                    # Strip whitespace from both ends and write to respective files
                    input_outfile.write(parts[0].strip() + '\n')
                    rec_outfile.write(parts[1].strip() + '\n')
                else:
                    # Handle lines that don't contain the delimiter
                    print(f"Warning: Delimiter not found in line: {line.strip()}")
                    input_outfile.write(line.strip() + '\n') # Write original line to input.txt if delimiter not found

    except FileNotFoundError:
        print(f"Error: One of the files not found. Please check paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define file paths relative to the project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'Data')

    input_file = os.path.join(data_dir, 'prompt_ADM.txt')
    output_input_file = os.path.join(data_dir, 'input.txt')
    output_recommendations_file = os.path.join(data_dir, 'recommendations.txt')

    # The specified delimiter
    text_delimiter = "and based on his or her listened music history, the top 10 recommended item is in the following:"

    process_prompt_data(input_file, output_input_file, output_recommendations_file, text_delimiter)
    print("Processing complete. Check 'Data/input.txt' and 'Data/recommendations.txt'.")
