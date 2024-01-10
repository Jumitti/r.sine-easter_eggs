file1_path = "output/unique_pictures.txt"
file2_path = "output_v2/unique_pictures.txt"
output_file_path = "special_words/compilation_unique_pictures.txt"

with open(file1_path, 'r') as file1:
    lines_file1 = set(file1.read().splitlines())

with open(file2_path, 'r') as file2:
    lines_file2 = set(file2.read().splitlines())

merged_lines = lines_file1.union(lines_file2)

with open(output_file_path, 'w') as output_file:
    output_file.write('\n'.join(merged_lines))

print(f"Fusion ended successfully : {output_file_path}")
