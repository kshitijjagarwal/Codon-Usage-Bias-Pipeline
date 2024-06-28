# Define the filename of the .rst file, it will be rst only btw ;)
filename = 'rst'

# Read the file content
with open(filename, 'r') as file:
    content = file.read()

# Define the start and end markers
start_marker = "List of extant and reconstructed sequences"
end_marker = "Overall accuracy"

# Find the positions of the start and end markers
start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

# Extract the relevant part of the text
if start_pos != -1 and end_pos != -1:
    extracted_content = content[start_pos:end_pos]
else:
    extracted_content = "Markers not found in the content."

# Define the path for the new file to save the extracted content, by default t will save in the same folder if path not mentioned
extracted_file_path = 'extracted_content.txt'

# Save the extracted content to the new file
with open(extracted_file_path, 'w') as extracted_file:
    extracted_file.write(extracted_content)

print(f"Extracted content has been saved to {extracted_file_path}")
