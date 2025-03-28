from Bio import SeqIO
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

def calcular_frequencia_dinucleotideos(sequencia):
    contador = Counter()
    for i in range(len(sequencia) - 1):
        dinucleotideo = str(sequencia[i:i+2])
        contador[dinucleotideo] += 1
    total_dinucleotideos = sum(contador.values())
    frequencias = {dinucleotideo: contagem / total_dinucleotideos for dinucleotideo, contagem in contador.items()}
    return frequencias

def analisar_fasta(arquivo_fasta):
    frequencias_list = []
    ids = []
    for record in SeqIO.parse(arquivo_fasta, "fasta"):
        frequencias = calcular_frequencia_dinucleotideos(record.seq)
        frequencias_list.append(frequencias)
        ids.append(record.id)
    return frequencias_list, ids

def calcular_matriz_distancias(frequencias_list):
    dinucleotideos = sorted(set(d for f in frequencias_list for d in f))
    matriz = np.zeros((len(frequencias_list), len(dinucleotideos)))
    for i, frequencias in enumerate(frequencias_list):
        for j, dinucleotideo in enumerate(dinucleotideos):
            matriz[i, j] = frequencias.get(dinucleotideo, 0)
    return matriz

def plotar_dendrograma(matriz, ids):
    Z = linkage(matriz, 'ward')
    plt.figure(figsize=(10, 6))
    dendrogram(Z, labels=ids, leaf_rotation=90)
    plt.xlabel('Sequências')
    plt.ylabel('Distância')
    plt.title('Dendrograma de Viés de Dinucleotídeos')
    plt.tight_layout()
    plt.show()

# Exemplo de uso
arquivo_fasta = "C:\\Users\\Administrator\\Desktop\\Jessica\\dinuclseqs.fasta"
frequencias_list, ids = analisar_fasta(arquivo_fasta)
matriz_distancias = calcular_matriz_distancias(frequencias_list)
plotar_dendrograma(matriz_distancias, ids)



