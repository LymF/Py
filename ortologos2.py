import re
import csv

def extract_gene_name(annotation):
    """Extrai o nome do gene da anotação."""
    match = re.search(r'ID=(.*?);', annotation)
    if match:
        return match.group(1)
    return None

def extract_orthologs_annotation(input_orthologs_file, input_annotation_file, output_file):
    orthologs_genes = set()  # Conjunto para armazenar os genes ortólogos
    annotation_data = {}  # Dicionário para armazenar os dados de anotação

    # Lendo a tabela de ortólogos e armazenando os genes ortólogos
    with open(input_orthologs_file, 'r') as ortho_file:
        reader = csv.reader(ortho_file, delimiter='\t')
        for row in reader:
            orthologs_genes.add(row[1].strip())

    print("Genes ortólogos:", orthologs_genes)

    # Lendo a tabela de anotação e armazenando os dados relevantes
    with open(input_annotation_file, 'r') as annotation_file:
        reader = csv.reader(annotation_file, delimiter='\t')
        header = next(reader)  # Lendo o cabeçalho
        print("Cabeçalho:", header)
        for row in reader:
            gene_name = extract_gene_name(row[8])  # Coluna 9 com a anotação
            start_coord = int(row[3]) - 1  # Subtraindo 1 da coordenada inicial
            end_coord = row[4]  # Coluna 5 com o fim da coordenada
            if gene_name in orthologs_genes:
                annotation_data[gene_name] = f"{start_coord}-{end_coord}"
                print("Coordenadas:", gene_name, start_coord, end_coord)
    
    # Escrevendo os resultados em uma nova tabela
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(["Gene", "Coordenadas"])  # Cabeçalho da nova tabela
        for gene, coords in annotation_data.items():
            writer.writerow([gene, coords])

# Exemplo de uso
input_orthologs_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\Ttru__v__dmelfiltrados.tsv'  # Substitua pelo caminho do arquivo de ortólogos
input_annotation_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\anotacao.tsv'  # Substitua pelo caminho do arquivo de anotação
output_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\resultado_anotacao_ortologos.tsv'  # Nome do arquivo de saída

extract_orthologs_annotation(input_orthologs_file, input_annotation_file, output_file)
