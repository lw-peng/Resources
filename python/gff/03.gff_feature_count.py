import argparse
from collections import defaultdict

"""
python 03.gff_feature_count.py input.gff output.txt
"""

def parse_gff3(gff3_file_path):
    gene_counts = defaultdict(lambda: {"mRNA": 0, "lnc_RNA": 0, "exon": 0, "CDS": 0})

    with open(gff3_file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue

            parts = line.strip().split("\t")
            if len(parts) < 9:
                continue

            feature_type = parts[2]
            attributes = parts[8]

            attr_dict = {attr.split("=")[0]: attr.split("=")[1] for attr in attributes.split(";") if "=" in attr}
            
            if feature_type in ["mRNA", "lnc_RNA", "exon", "CDS"]:
                if "gene" in attr_dict:
                    parent_gene = attr_dict["gene"]
                    gene_counts[parent_gene][feature_type] += 1

    return gene_counts

def main():
    parser = argparse.ArgumentParser(description="Parse GFF3 files to count mRNA, exon, and CDS for each gene.")
    parser.add_argument("gff3_file_path", type=str, help="Path to the GFF3 file.")
    parser.add_argument("output_file_path", type=str, help="Path to the output text file.")

    args = parser.parse_args()

    gene_counts = parse_gff3(args.gff3_file_path)

    with open(args.output_file_path, 'w') as out_file:
        for gene_id, counts in gene_counts.items():
            out_file.write(f"{gene_id}\t{counts['mRNA']}\t{counts['lnc_RNA']}\t{counts['exon']}\t{counts['CDS']}\n")
    
    print(f"Results saved to {args.output_file_path}")

if __name__ == "__main__":
    main()
