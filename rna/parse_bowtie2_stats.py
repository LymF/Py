import os
import re

def parse_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extrair todas as linhas do arquivo e removendo quebras de linha
    data = [line.strip() for line in lines]

    return data

def main():
    # Diretório onde os arquivos txt estão localizados
    directory = 'c:\\Users\\Administrator\\Desktop\\Bowtie2'

    # Nome do arquivo tsv onde os dados serão salvos
    output_file = 'c:\\Users\\Administrator\\Desktop\\Bowtie2\\mappingstatisticstable.tsv'

    with open(output_file, 'w') as tsv_file:
        tsv_file.write("Folder_Condition\tData\n")  # Cabeçalho do arquivo TSV

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith("_mapping_summary.txt"):
                    folder_name = os.path.basename(root)  # Nome da pasta
                    file_path = os.path.join(root, file)
                    condition_prefix = file.split("_")[0]  # Prefixo do nome do arquivo txt
                    data = parse_txt_file(file_path)
                    tsv_file.write(f"{folder_name}_{condition_prefix}\t")
                    tsv_file.write('\t'.join(data) + '\n')

    print("Dados transferidos para", output_file)

if __name__ == "__main__":
    main()
