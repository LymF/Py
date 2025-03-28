import os
import pandas as pd

def filter_and_save(input_file, output_file):
    # Lê o arquivo tabular
    df = pd.read_csv(input_file, sep='\t')
    
    # Filtra as linhas que contêm a palavra "virus" na 25ª coluna
    filtered_df = df[df.iloc[:, 24].str.contains('virus', case=False, na=False)]
    
    # Salva o arquivo filtrado
    filtered_df.to_csv(output_file, sep='\t', index=False)

# Substitua 'input_folder' pelo caminho da pasta que contém os arquivos tabulares
input_folder = "C:\\Users\\Administrator\\Desktop\\Anderson\\filtradovirus"

# Substitua 'output_folder' pelo caminho da pasta onde os arquivos filtrados serão salvos
output_folder = "C:\\Users\\Administrator\\Desktop\\Anderson\\filtradovirus"

# Loop pelos arquivos na pasta de entrada
for file_name in os.listdir(input_folder):
    if file_name.endswith('.tabular'):
        # Caminho completo do arquivo de entrada
        input_file_path = os.path.join(input_folder, file_name)
        
        # Caminho completo do arquivo de saída
        output_file_path = os.path.join(output_folder, file_name)
        
        # Chama a função para filtrar e salvar
        filter_and_save(input_file_path, output_file_path)

print("Operação concluída!")
