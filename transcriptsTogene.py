def map_transcripts_to_genes(transcript_table_file, mapping_table_file, output_file):
    # Ler a segunda tabela de mapeamento e armazenar o mapeamento de transcritos para genes em um dicionário
    transcript_to_gene = {}
    with open(mapping_table_file, 'r') as mapping_file:
        for line in mapping_file:
            fields = line.strip().split('\t')
            if len(fields) >= 2:
                transcript_id = fields[1]  # Assume que o ID do transcrito está na segunda coluna
                gene_id = fields[0]  # Assume que o ID do gene está na primeira coluna
                transcript_to_gene[transcript_id] = gene_id

    # Abrir o arquivo de saída para escrita
    with open(output_file, 'w') as output:
        # Ler a primeira tabela de transcritos e substituir os IDs de transcritos pelos IDs de genes correspondentes
        with open(transcript_table_file, 'r') as transcript_file:
            for line in transcript_file:
                parts = line.strip().split('\t')
                transcript_id = parts[0]  # Assume que o ID do transcrito está na primeira coluna
                gene_id = transcript_to_gene.get(transcript_id, transcript_id)  # Obter o ID do gene correspondente ou manter o ID do transcrito
                output.write(gene_id + '\t' + '\t'.join(parts[1:]) + '\n')  # Escrever a linha com o ID do gene substituído e o restante das partes

# Caminho para o arquivo da primeira tabela de transcritos
transcript_table_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\countsgenesdrosophilaabm_sem_duplicatas.tsv'

# Caminho para o arquivo da segunda tabela de mapeamento
mapping_table_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\fbgn_fbtr_fbpp_fb_2024_01.tsv'

# Caminho para o arquivo de saída
output_file = 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\countsdrosophilagenefinalabm.tsv'

# Realizar o mapeamento e salvar o resultado
map_transcripts_to_genes(transcript_table_file, mapping_table_file, output_file)
