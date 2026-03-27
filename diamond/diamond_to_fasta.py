import pandas as pd
import os

# Diretório contendo os arquivos XLSX
input_dir = "C:\\Users\\Administrator\\Desktop\\dali"

# Diretório de saída para os arquivos FASTA
output_dir = "C:\\Users\\Administrator\\Desktop\\dali"

# Certifique-se de que o diretório de saída exista, se não, crie-o
os.makedirs(output_dir, exist_ok=True)

# Iterar sobre todos os arquivos no diretório de entrada
for filename in os.listdir(input_dir):
    
    # Verificar se o arquivo é um XLSX
    if filename.endswith(".xlsx"):
        # Construir o caminho completo para o arquivo XLSX
        caminho_arquivo_excel = os.path.join(input_dir, filename)

        # Ler o arquivo XLSX em um DataFrame do pandas
        df = pd.read_excel(caminho_arquivo_excel)

        # Criar o nome do arquivo de saída com a extensão .fasta
        output_file_name = os.path.splitext(filename)[0] + ".fasta"
        output_file_path = os.path.join(output_dir, output_file_name)

        # Iterar sobre as linhas do DataFrame e criar um arquivo FASTA para cada linha
        with open(output_file_path, "w") as fasta_file:
            for index, row in df.iterrows():
                header = ">" + str(row.iloc[26])  # Primeira coluna como cabeçalho
                sequence = str(row.iloc[12])     # Décima sexta coluna como sequência

                # Escrever o cabeçalho e a sequência no arquivo FASTA
                fasta_file.write(header + "\n" + sequence + "\n")

    # Código para arquivos TSV (comentado)
    # elif filename.endswith(".tsv"):
    #     # Construir o caminho completo para o arquivo TSV
    #     caminho_arquivo_tsv = os.path.join(input_dir, filename)
    
    #     # Ler o arquivo TSV em um DataFrame do pandas
    #     df = pd.read_csv(caminho_arquivo_tsv, sep='\t')

    #     # Criar o nome do arquivo de saída com a extensão .fasta
    #     output_file_name = os.path.splitext(filename)[0] + ".fasta"
    #     output_file_path = os.path.join(output_dir, output_file_name)

    #     # Iterar sobre as linhas do DataFrame e criar um arquivo FASTA para cada linha
    #     with open(output_file_path, "w") as fasta_file:
    #         for index, row in df.iterrows():
    #             header = ">" + str(row.iloc[1])  # Primeira coluna como cabeçalho
    #             sequence = str(row.iloc[15])     # Décima sexta coluna como sequência

    #             # Escrever o cabeçalho e a sequência no arquivo FASTA
    #             fasta_file.write(header + "\n" + sequence + "\n")

print("Arquivos FASTA criados com sucesso!")
