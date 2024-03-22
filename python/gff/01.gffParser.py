import argparse
import gzip

"""
python process_gff.py -i /path/to/your.gff or your.gff.gz -o /path/to/output.txt -g genome_name
"""

def parse_gff(gff_file_path, genome_name):
    genes_info = []

    # Determine if the file is gzipped based on its extension
    if gff_file_path.endswith('.gz'):
        open_func = gzip.open
    else:
        open_func = open

    with open_func(gff_file_path, 'rt') as file:  # 'rt' mode for reading text from potentially compressed files
        for line in file:
            if not line.startswith('#') and line.strip():
                parts = line.split('\t')
                if parts[2] == 'gene':
                    chromosome = parts[0]
                    start_position = int(parts[3])
                    end_position = int(parts[4])
                    strand = parts[6]
                    attributes = parts[8]
                    
                    attributes_dict = {item.split('=')[0]: item.split('=')[1] for item in attributes.split(';') if '=' in item}
                    gene_name = attributes_dict.get('ID', 'Unknown').replace('gene-', '')

                    gene_length = end_position - start_position + 1
                    expanded_start_position = start_position - 500
                    expanded_end_position = end_position + 500
                    genes_info.append((gene_name, genome_name, chromosome, start_position, end_position, gene_length, strand, f"{chromosome}:{expanded_start_position}..{expanded_end_position}"))

    return genes_info

def main():
    parser = argparse.ArgumentParser(description='Parse GFF or GFF.GZ file and extract gene information.')
    parser.add_argument('-i', '--input_gff', required=True, help='Path to the GFF or GFF.GZ file.')
    parser.add_argument('-o', '--output_file', required=True, help='Path to the output TXT file.')
    parser.add_argument('-g', '--genome_name', type=str, required=True, help='Name of the genome')

    args = parser.parse_args()

    genes_info = parse_gff(args.input_gff, args.genome_name)

    with open(args.output_file, 'w') as out_file:
        for info in genes_info:
            out_file.write(f"{info[0]}\t{info[1]}\t{info[2]}\t{info[3]}\t{info[4]}\t{info[5]}\t{info[6]}\t{info[7]}\n")

if __name__ == '__main__':
    main()
