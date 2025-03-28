import csv

def replace_gene_names(input_orthologs_file, input_counts_file, output_file):
    orthologs_genes = {}  # Dicionário para armazenar os genes ortólogos de Drosophila e T. truncatus

    # Lendo a tabela de ortólogos e armazenando os genes ortólogos
    with open(input_orthologs_file, 'r') as ortho_file:
        reader = csv.reader(ortho_file, delimiter='\t')
        for row in reader:
            drosophila_gene = row[1]
            truncatus_gene = row[2].split('-')[0]  # Obtendo o nome do gene de T. truncatus antes do hífen
            if truncatus_gene not in orthologs_genes:
                orthologs_genes[truncatus_gene] = drosophila_gene
            else:
                orthologs_genes[truncatus_gene] = drosophila_gene  # Atualiza o ortólogo caso haja mais de um

    # Lendo a tabela de contagens e substituindo os nomes dos genes de T. truncatus pelos de Drosophila
    with open(input_counts_file, 'r') as counts_file:
        reader = csv.reader(counts_file)
        with open(output_file, 'w', newline='') as outfile:
         writer = csv.writer(outfile, delimiter='\t')
         for row in reader:
            truncatus_gene = row[0].split('-')[0]  # Obtendo o nome do gene de T. truncatus antes do hífen
            if truncatus_gene in orthologs_genes:
                drosophila_gene = orthologs_genes[truncatus_gene]
                row[0] = drosophila_gene
                writer.writerow(row)
                del orthologs_genes[truncatus_gene]  # Removendo o gene ortólogo já utilizado


# Exemplo de uso
input_orthologs_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\dmel__v__Ttrufiltrados.tsv'  # Substitua pelo caminho do arquivo de ortólogos
input_counts_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\counts_corrigidosabm.csv'  # Substitua pelo caminho do arquivo de contagens
output_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\countsgenesdrosophilaabm.tsv'  # Nome do arquivo de saída

replace_gene_names(input_orthologs_file, input_counts_file, output_file)
