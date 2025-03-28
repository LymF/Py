import pandas as pd

# Função para ler e processar uma tabela
def ler_tabela(caminho_arquivo):
    try:
        tabela = pd.read_csv(caminho_arquivo)
        return tabela
    except Exception as e:
        print(f"Erro ao ler a tabela {caminho_arquivo}: {e}")
        return None

# Função para comparar as vias e calcular o enriquecimento total
def comparar_vias(tabela1, tabela2, tabela3):
    # Unir as tabelas usando o nome das vias como índice
    merge_tabelas = pd.merge(tabela1, tabela2, on='vias', how='outer', suffixes=('_tabela1', '_tabela2'))
    merge_tabelas = pd.merge(merge_tabelas, tabela3, on='vias', how='outer')

    return merge_tabelas

# Ler as tabelas
tabela1 = ler_tabela('c:\\Users\\Administrator\\Desktop\\Iwtop20heatmap.csv')
tabela2 = ler_tabela('c:\\Users\\Administrator\\Desktop\\Istop20heatmap.csv')
tabela3 = ler_tabela('c:\\Users\\Administrator\\Desktop\\Iwstop20heatmap.csv')

# Verificar se as tabelas foram lidas com sucesso
if tabela1 is not None and tabela2 is not None and tabela3 is not None:
    # Comparar as vias e calcular o enriquecimento total
    nova_tabela = comparar_vias(tabela1, tabela2, tabela3)

    # Definir o nome do arquivo de saída e seu caminho
    caminho_saida = 'c:\\Users\\Administrator\\Desktop\\nova_tabela.csv'

    # Escrever a nova tabela no arquivo especificado
    nova_tabela.to_csv(caminho_saida, index=False)

    print(f"A nova tabela foi salva em: {caminho_saida}")
else:
    print("Erro ao ler uma ou mais tabelas.")
