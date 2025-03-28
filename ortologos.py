import pandas as pd     

import csv

def organize_orthologs(input_file, output_file):
    """Organiza a tabela de ortólogos."""
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        for row in reader:
            genes_species1 = row[1].split(',')[:10]  # Pegando no máximo 10 genes da coluna 2
            genes_species2 = row[2].split(',')[:10]  # Pegando no máximo 10 genes da coluna 3
            for gene1 in genes_species1:
                for gene2 in genes_species2:
                    writer.writerow([row[0], gene1.strip(), gene2.strip()])

# Exemplo de uso
input_file = 'c:\\Users\\Administrator\\Desktop\\dmel__v__Ttru.tsv'  # Substitua 'ortologos.tsv' pelo caminho do seu arquivo TSV
output_file = 'c:\\Users\\Administrator\\Desktop\\dmel__v__Ttrufiltrados.tsv'  # Nome do arquivo de saída organizado
organize_orthologs(input_file, output_file)
