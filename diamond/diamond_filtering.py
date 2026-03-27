import openpyxl as op
import re
import pandas as pd
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from time import sleep
import os
import subprocess

# Configuração inicial
#caminho_arquivo = "C:\\Users\\Administrator\\Desktop\\evepip\\evesparadoxa.tabular"  # Substitua pelo caminho do arquivo de entrada
#local_virus = "C:\\Users\\Administrator\\Desktop\\evepip\\ICTV_Master_Species_List_2022_MSL38.v2.xlsx"  # Substitua pelo caminho do arquivo ICTV
#caminho_db_diamond = "C:\\Users\\Administrator\\Desktop\\evepip\\viraldb.dmnd"  # Substitua pelo caminho do banco de dados do DIAMOND
caminho_arquivo = "/home/lucas/evepipe/evesparadoxa.tabular"  # Substitua pelo caminho do arquivo de entrada
local_virus = "/home/lucas/evepipe/ICTV_Master_Species_List_2022_MSL38.v2.xlsx"  # Substitua pelo caminho do arquivo ICTV
caminho_db_diamond = "/home/lucas/evepipe/viraldb.dmnd"  # Substitua pelo caminho do banco de dados do DIAMOND
Entrez.email = 'jp.uesc17@gmail.com'
Entrez.api_key = 'ee7ccfdfa22559163c2bd8f3c822157ae108'
cache_path = "cache_ncbi.json"


data = {}
data_genome = {}

def get_ncbi_tax(taxon):
    try:
        '''Obtém a taxonomia do NCBI'''
        if not re.match(r'\d+', taxon):
            taxon2 = '"' + taxon + '"'
            handle = Entrez.esearch(db='taxonomy', term=taxon2, rettype='gb', retmode='text')
            record = Entrez.read(handle, validate=False)
            handle.close()
            if not record['IdList']:
                return None
            tax_id = record['IdList']
        else:
            tax_id = taxon

        handle2 = Entrez.efetch(db='taxonomy', id=tax_id, retmode='xml')
        record2 = Entrez.read(handle2, validate=False)
        handle2.close()

        tax_list = record2[0]['LineageEx']
        for tax_element in tax_list:
            if tax_element['Rank'] == 'family':
                return tax_element['ScientificName']
        return None
    except Exception as e:
        print(f"Erro ao consultar taxonomia para {taxon}: {e}")
        return None

def identificar_taxons(caminho_tabela):
    """
    Identifica os táxons usando o NCBI e o ICTV Master Species List.
    """
    lt_ICTV = pd.read_excel(local_virus, sheet_name='MSL')
    coluna_familia = lt_ICTV['Family']
    coluna_genoma = lt_ICTV['Genome Composition']

    tabela = pd.read_csv(caminho_tabela, sep="\t", header=None)
    lista_adict = []
    lista_adct2 = []

    for especie in tabela[14]:
        if especie in data:
            lista_adict.append(data[especie])
        else:
            taxonomia = get_ncbi_tax(especie)
            lista_adict.append(taxonomia)
            data[especie] = taxonomia

    for familia in lista_adict:
        if familia in data_genome:
            lista_adct2.append(data_genome[familia])
        else:
            match = lt_ICTV[lt_ICTV['Family'] == familia]
            if not match.empty:
                genoma = match.iloc[0]['Genome Composition']
                data_genome[familia] = genoma
                lista_adct2.append(genoma)
            else:
                lista_adct2.append(None)

    tabela['Familia'] = lista_adict
    tabela['Genoma'] = lista_adct2

    caminho_saida = caminho_tabela.replace('.tabular', '_taxons_identificados.xlsx')
    tabela.to_excel(caminho_saida, index=False)
    print(f"Tabela com identificação de táxons salva como: {caminho_saida}")
    return caminho_saida

def extracao(caminho_arquivo):
    """
    Processa a saída do DIAMOND para filtrar os melhores hits com base em e-value e bitscore.
    Salva os resultados em um arquivo Excel com sufixo '_hitfiltered'.
    """
    # Lendo o arquivo tabular
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    banco_entrada = []
    banco_saida = []

    # Transformando as linhas em listas de colunas
    for linha in linhas:
        banco_entrada.append(linha.strip().split('\t'))

    # Filtrando os melhores hits
    for i in banco_entrada:
        if i == banco_entrada[0]:
            banco_saida.append(i)
        elif i[0] in banco_saida[-1]:
            if float(i[11]) < float(banco_saida[-1][11]):
                banco_saida[-1] = i
            elif float(i[11]) == float(banco_saida[-1][11]):
                if float(i[12]) > float(banco_saida[-1][12]):
                    banco_saida[-1] = i
        else:
            banco_saida.append(i)

    # Salvando os resultados em um arquivo Excel
    nome_saida = caminho_arquivo.replace('.tabular', '_hitfiltered.xlsx')
    book = op.Workbook()
    lista_page = book.active
    lista_page.title = "Filtered Hits"

    for linha in banco_saida:
        lista_page.append(linha)

    book.save(nome_saida)
    print(f"Arquivo salvo como: {nome_saida}")
    print(f"Quantidade de ORFs virais filtrados: {len(banco_saida)}")

def tabela_para_fasta(caminho_tabela, caminho_fasta):
    """
    Converte uma tabela em formato Excel para um arquivo FASTA.
    - A coluna 0 será usada como identificador.
    - A coluna 16 será usada como sequência.
    """
    tabela = pd.read_excel(caminho_tabela, header=None)
    registros = []

    for _, linha in tabela.iterrows():
        identificador = linha[0]  # Coluna do identificador (modifique se necessário)
        sequencia = linha[16]  # Coluna da sequência (modifique se necessário)
        registros.append(SeqRecord(Seq(sequencia), id=str(identificador), description=""))

    SeqIO.write(registros, caminho_fasta, "fasta")
    print(f"FASTA gerado: {caminho_fasta}")

def executar_cdhit(caminho_fasta):
    """
    Executa o CD-HIT para clusterizar sequências e reduzir redundância.
    """
    saida_cdhit = caminho_fasta.replace('.fasta', '_cdhit.fasta')
    comando = [
        "cd-hit", "-i", caminho_fasta, "-o", saida_cdhit, "-c", "0.9", "-n", "5",
        "-M", "400", "-d", "0", "-T", "2"
    ]
    subprocess.run(comando)
    print(f"CD-HIT concluído. Saída: {saida_cdhit}")
    return saida_cdhit

def fasta_para_tabela(caminho_fasta, caminho_tabela):
    """
    Converte um arquivo FASTA para uma tabela usando DIAMOND.
    """
    comando = [
        "diamond", "blastx", "--query", caminho_fasta, "--db", caminho_db_diamond,
        "--out", caminho_tabela, "--outfmt", "6",
        "qseqid", "sseqid", "qlen", "slen", "pident", "length", "mismatch", "gapopen",
        "qstart", "qend", "sstart", "send", "evalue", "bitscore", "stitle", "qtitle", "full_qseq",
        "--max-target-seqs", "1"
    ]
    subprocess.run(comando)
    print(f"DIAMOND concluído. Saída: {caminho_tabela}")

def filtrar_proteinas(caminho_tabela):
    """
    Filtra hits com base em proteínas de interesse.
    """
    proteinas_interesse = re.compile(
        r"RdRp|RNA-dependent RNA polymerase|capsid|coat|replicase|glycoprotein|nucleoprotein|nucleocapsid"
    )

    tabela = pd.read_csv(caminho_tabela, sep="\t", header=None)
    tabela_filtrada = tabela[tabela[14].str.contains(proteinas_interesse, na=False)]  # Coluna 14 contém o título da sequência

    caminho_saida = caminho_tabela.replace('.tabular', '_proteins_filtered.tabular')
    tabela_filtrada.to_csv(caminho_saida, sep="\t", index=False, header=False)
    print(f"Tabela filtrada por proteínas de interesse salva como: {caminho_saida}")
    return caminho_saida

if __name__ == "__main__":
    try:
        # 1. Filtrar melhores hits
        extracao(caminho_arquivo)

        # 2. Converter para FASTA
        caminho_fasta = caminho_arquivo.replace('.tabular', '_hitfiltered.fasta')
        tabela_para_fasta(caminho_arquivo.replace('.tabular', '_hitfiltered.xlsx'), caminho_fasta)

        # 3. Executar CD-HIT
        saida_cdhit = executar_cdhit(caminho_fasta)

        # 4. Converter de volta para tabela
        caminho_tabela_diamond = saida_cdhit.replace('.fasta', '_diamond.tabular')
        fasta_para_tabela(saida_cdhit, caminho_tabela_diamond)

        # 5. Filtrar por proteínas de interesse
        caminho_filtrado_proteinas = filtrar_proteinas(caminho_tabela_diamond)

        # 6. Identificar táxons com base no NCBI e ICTV
        caminho_identificado_taxons = identificar_taxons(caminho_filtrado_proteinas)

        print("Processo concluído com sucesso!")
    except Exception as e:
        print(f"Erro no processamento: {e}")
