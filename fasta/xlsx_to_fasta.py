import pandas as pd

def excel_to_fasta(input_file, output_file, header_column_index, sequence_column_index):
    """
    Converte duas colunas de um arquivo Excel (.xlsx) em um arquivo FASTA.
    
    Args:
        input_file (str): Caminho para o arquivo Excel de entrada.
        output_file (str): Caminho para o arquivo FASTA de saída.
        header_column_index (int): Índice da coluna que será usada como header do FASTA (começa de 0).
        sequence_column_index (int): Índice da coluna que contém as sequências (começa de 0).
    """
    # Carregar o arquivo Excel
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Erro ao carregar o arquivo Excel: {e}")
        return

    # Verificar se os índices das colunas são válidos
    if header_column_index >= len(df.columns) or sequence_column_index >= len(df.columns):
        print("Erro: Os índices das colunas especificados estão fora do intervalo.")
        return

    # Abrir o arquivo de saída para escrita
    with open(output_file, 'w') as fasta_file:
        for _, row in df.iterrows():
            header = row.iloc[header_column_index]
            sequence = row.iloc[sequence_column_index]
            
            # Escrever no formato FASTA
            fasta_file.write(f">{header}\n{sequence}\n")
    
    print(f"Arquivo FASTA gerado com sucesso em: {output_file}")

# Exemplo de uso
excel_to_fasta(
    input_file="/home/lucas/Documents/papers/bombus/seqs-eves.xlsx", 
    output_file="/home/lucas/Documents/papers/bombus/eves.fasta", 
    header_column_index= 0,  # Índice da coluna para o header
    sequence_column_index= 1  # Índice da coluna para a sequência
)
