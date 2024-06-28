import os

def extract_text(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        content = file.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(content):
        if 'Ancestral reconstruction by CODONML.' in line:
            start_index = i
        if 'tree with node labels for Rod Page\'s TreeView' in line:
            end_index = i + 2  # Including the line below this line

    if start_index != -1 and end_index != -1:
        extracted_text = content[start_index:end_index]
        extracted_text = ''.join(extracted_text)
    else:
        extracted_text = "The required text was not found in the file."

    # Save the extracted text to a file
    with open(output_file_path, 'w') as output_file:
        output_file.write(extracted_text)

    print(f"Extracted text saved to {output_file_path}")

if __name__ == "__main__":
    input_file_path = "rst"
    output_file_path = "relation.txt"
    extract_text(input_file_path, output_file_path)
