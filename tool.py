import re
import argparse

def transform_markdown(markdown: str) -> str:
    # Define a mapping from original keywords to new formats
    mapping = {
        'flag': 'tip',
        'comment': 'info',
        'question': 'info',
        'option': 'info',
        'todo': 'warning',
        'danger': 'danger',
        'caution': 'danger'
    }
    
    # Define the regex pattern for matching the entire block
    # This pattern captures three groups:
    # 1. (\w+): Matches any word (keyword) following '####' and captures it as the block type.
    # 2. (.*?): Matches the title after the keyword, using non-greedy matching to stop at the first newline.
    # 3. ((?:>.*?\n|>\s*\n)+): Matches the content block, which consists of lines starting with '> '.
    #    - (?:>.*?\n): Matches lines starting with '>', followed by any characters, ending in newline.
    #    - (?:>\s*\n): Matches lines that contain only '>' followed by optional whitespace and a newline.
    #    - +: Ensures that one or more such lines are matched.
    pattern = r'> #### (\w+)::(.*?)\n((?:>.*?\n|>\s*\n)+)'

    # Function to replace matched patterns with the desired format
    def replace_block(match):
        block_type = match.group(1)  # Extract block type (any keyword)
        title = match.group(2).strip()  # Extract the title
        new_format = mapping.get(block_type, 'info')  # Look up the new format based on the block type using the mapping
        content = match.group(3).replace('>\n', '\n').replace('> ', '').strip()  # Clean content lines
        return f':::{new_format}[{title}]\n{content}\n:::'  # Format block

    transformed_markdown = re.sub(pattern, replace_block, markdown, flags=re.DOTALL)
    return transformed_markdown

def main(input_file, output_file=None, inplace=False):
    # Read the content of the input markdown file
    with open(input_file, 'r', encoding='utf-8') as infile:
        markdown_content = infile.read()

    # Transform the content using the transform_markdown function
    transformed_content = transform_markdown(markdown_content)

    # Check if inplace editing is enabled
    if inplace:
        # Write the transformed content back to the input file
        with open(input_file, 'w', encoding='utf-8') as outfile:
            outfile.write(transformed_content)
    elif output_file:
        # Write the transformed content to the specified output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(transformed_content)
    else:
        # Print the transformed content to stdout
        print(transformed_content)  # Print to stdout if no output file is specified

if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Transform markdown sections into a new format.')
    parser.add_argument('input_file', type=str, help='Path to the input markdown file')
    parser.add_argument('-o', '--output_file', type=str, help='Path to the output markdown file')
    parser.add_argument('-i', '--inplace', action='store_true', help='Edit the input file in place')  # Short flag for in-place editing
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Call the main function with parsed arguments
    main(args.input_file, args.output_file, args.inplace)
