"""import pandas as pd

table = read.csv('c:\\Users\\Administrator\\Desktop\\Ortogolos\\countsgenesdrosophilateste.tsv')

lista  = []

for i in range (len(table)) :
    
    if len(lista) == 0:
       
        lista.append(table[0][i])

    else: 
        if table[0][i] not in lista:

            lista.append(table[0][i])
    
        else:
            if 
            """
            

import pandas as pd

# Ler a tabela
table = pd.read_csv('c:\\Users\\Administrator\\Desktop\\Ortogolos\\countsgenesdrosophilatemp.tsv', delimiter='\t')

# Remover linhas duplicadas na primeira coluna
table_sem_duplicatas = table.drop_duplicates(subset=table.columns[0])

# Salvar a tabela sem duplicatas
table_sem_duplicatas.to_csv('c:\\Users\\Administrator\\Desktop\\Ortogolos\\countsgenesdrosophilatemp_sem_duplicatas.tsv', sep='\t', index=False)

        