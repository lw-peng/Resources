# 01.gffParser.py
## description：
- 解析gff3文件。
- 提取以下信息：
  - geneID  genome_name  chromosome  start  end  strand  length  chromosome:expanded_start..expanded_end

# 02.chromosome_rename.py
## description：
- 解析gff3文件生成的bed格式文件，将染色体替换为chr1..格式。
- 理论上任意bed格式文件都行，只替换其中的染色体号。

# 03.gff_feature_count.py
## description:
- 解析gff3文件中，每个gene的mRNA，lnc_RNA，exon，CDS的数量。
- 提取格式为：
  - geneID mRNA_count lnc_RNA_count exon_count CDS_count
