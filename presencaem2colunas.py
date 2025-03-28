import pandas as pd

# Caminho para o arquivo da primeira tabela
tabela1_path = 'c:\\Users\\Administrator\\Desktop\\ArquivosR\\differential_geneswolbachia.xlsx'

# Caminho para o arquivo da segunda tabela
tabela2_path = 'c:\\Users\\Administrator\\Desktop\\ArquivosR\\differential_genesspiroplasma.xlsx'

# Carregar os arquivos das duas tabelas
tabela1 = pd.read_excel(tabela1_path)
tabela2 = pd.read_excel(tabela2_path)

# Extrair apenas os valores das colunas
tabela1_genes = tabela1.iloc[:, 0].astype(str).tolist()
tabela2_genes = tabela2.iloc[:, 0].astype(str).tolist()

# Encontrar os genes comuns
genes_comuns = list(set(tabela1_genes) & set(tabela2_genes))

# Encontrar genes exclusivos de cada tabela
genes_wolbachia_apenas = [gene for gene in tabela1_genes if gene not in genes_comuns]
genes_spiroplasma_apenas = [gene for gene in tabela2_genes if gene not in genes_comuns]

# Criar DataFrames para cada conjunto de genes
df_comuns = pd.DataFrame({"Common genes": genes_comuns})
df_wolbachia = pd.DataFrame({"Wolbachia only": genes_wolbachia_apenas})
df_spiroplasma = pd.DataFrame({"Spiroplasma only": genes_spiroplasma_apenas})

# Concatenar os DataFrames lado a lado
resultado = pd.concat([df_comuns, df_wolbachia, df_spiroplasma], axis=1)

# Salvar os resultados no arquivo de saída
resultado.to_csv('c:\\Users\\Administrator\\Desktop\\ArquivosR\\DEgenescorrelacionados.tsv', sep='\t', index=False)
