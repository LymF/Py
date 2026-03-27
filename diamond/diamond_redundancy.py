import pandas as pd

# Caminho para o novo arquivo tabular
caminho_arquivo = "C:\\Users\\Administrator\\Desktop\\Anderson\\SRR11260806blast.tabular"

# Ler o arquivo tabular em um DataFrame do pandas
df = pd.read_csv(caminho_arquivo, sep='\t')

# Ler a 15ª linha e a primeira coluna da tabela original
linha_15_primeira_coluna = pd.read_csv(caminho_arquivo, sep='\t', nrows=15, usecols=[0], header=None, names=['1']).iloc[0]

# Salvar a 15ª linha da tabela original na 15ª linha do DataFrame
df.iloc[14, 0] = linha_15_primeira_coluna['1']

# Classificar o DataFrame pelo valor na coluna 11 (e-value)
df = df.sort_values(by=df.columns[10])

# Criar uma máscara para manter apenas as linhas não redundantes
mascara = (
    ~df.duplicated(subset=[df.columns[0]], keep='last') | 
    (df[df.columns[0]] == linha_15_primeira_coluna['1'])
)

# Filtrar o DataFrame usando a máscara
df_filtrado = df[mascara]

# Atualizar o caminho do arquivo de saída para ter a extensão _filtrado.tabular
caminho_arquivo_filtrado = caminho_arquivo.replace('.tsv', '_filtrado.tsv')

# Salvar o DataFrame filtrado no novo arquivo tabular TSV
df_filtrado.to_csv(caminho_arquivo_filtrado, sep='\t', index=False)
