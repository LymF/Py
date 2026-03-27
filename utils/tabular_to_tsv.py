import pandas as pd

def convert_to_tsv(input_file, output_file):
    # Lê o arquivo tabular
    df = pd.read_csv(input_file, sep='\t')
    
    # Salva o arquivo como TSV
    df.to_csv(output_file, sep='\t', index=False)

# Substitua 'input_file.csv' pelo caminho do seu arquivo tabular
input_file = "C:\\Users\\Administrator\\Desktop\\Anderson\\SRR10741871blast.tabular"

# Substitua 'output_file.tsv' pelo nome do arquivo TSV de saída
output_file = 'C:\\Users\\Administrator\\Desktop\\Anderson\\SRR10741871blast.tsv'

# Chama a função para converter
convert_to_tsv(input_file, output_file)

print("Arquivo convertido com sucesso!")
