import argparse

"""
染色体号由 CM048153.1 --> CM048181.1 为例：
python3 03_chromosome_rename.py -i /path/to/input.txt -o /path/to/output.txt -p CM -s 48153 -e 48181 -m mapping.txt
"""

def generate_mapping(start, end, prefix, mapping_filename):
    with open(mapping_filename, "w") as mapping_file:
        for i in range(start, end + 1):
            chr_number = i - start + 1
            mapping_file.write("{}{:06d}.1\tchr{}\n".format(prefix, i, chr_number))

def update_txt(input_filename, mapping_filename, updated_filename):
    mapping = {}
    with open(mapping_filename, "r") as mapping_file:
        for line in mapping_file:
            old, new = line.strip().split('\t')
            mapping[old] = new

    with open(input_filename, "r") as infile, open(updated_filename, "w") as outfile:
        for line in infile:
            parts = line.strip().split('\t')
            if parts[0] in mapping:
                parts[0] = mapping[parts[0]]
            outfile.write('\t'.join(parts) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update text file chromosome numbers.')
    parser.add_argument('-i', '--input_filename', required=True, help='The text file to update.')
    parser.add_argument('-o', '--output_file', required=True, help='Path to the output TXT file')
    parser.add_argument('-s', '--start_number', type=int, required=True, help='The starting chromosome number (e.g., 48153 for CM048153.1).')
    parser.add_argument('-e', '--end_number', type=int, required=True, help='The ending chromosome number (e.g., 48181 for CM048181.1).')
    parser.add_argument('-p', '--prefix', default='CM', help='The prefix for the chromosome numbers (e.g., CM for CM048153.1). Default is CM.')
    parser.add_argument('-m', '--mapping_filename', default='mapping.txt', help='The filename for the chromosome number mapping. Default is mapping.txt.')
    args = parser.parse_args()

    updated_filename = args.output_file

    generate_mapping(args.start_number, args.end_number, args.prefix, args.mapping_filename)
    update_txt(args.input_filename, args.mapping_filename, updated_filename)

    print(f"Updated text file has been saved as {updated_filename}")
