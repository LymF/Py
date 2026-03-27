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
caminho_arquivo = "/home/lucas/evepip/SRR14087841-diamond.tabular"  # Caminho do arquivo de entrada
local_virus = "/home/lucas/evepip/ICTV_Master_Species_List_2022_MSL38.v2.xlsx"  # Caminho do arquivo ICTV
caminho_db_diamond = "/home/lucas/evepip/viraldb.dmnd"  # Caminho do banco de dados do DIAMOND
Entrez.email = 'jp.uesc17@gmail.com'
Entrez.api_key = 'ee7ccfdfa22559163c2bd8f3c822157ae108'

# Configurações ajustáveis pelo usuário
threads = 10  # Número de threads para CD-HIT e DIAMOND
memoria = 10000  # Memória máxima para CD-HIT (em MB)

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

def identificar_taxons(caminho_tabela, nome_base):
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

    caminho_saida = f"{nome_base}_taxons_identificados.xlsx"
    tabela.to_excel(caminho_saida, index=False)
    print(f"Tabela com identificação de táxons salva como: {caminho_saida}")
    return caminho_saida

def extracao(caminho_arquivo, nome_base):
    """
    Processa a saída do DIAMOND para filtrar os melhores hits com base em e-value e bitscore.
    """
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    banco_entrada = []
    banco_saida = []

    for linha in linhas:
        banco_entrada.append(linha.strip().split('\t'))

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

    nome_saida = f"{nome_base}_hitfiltered.xlsx"
    book = op.Workbook()
    lista_page = book.active
    lista_page.title = "Filtered Hits"

    for linha in banco_saida:
        lista_page.append(linha)

    book.save(nome_saida)
    print(f"Arquivo salvo como: {nome_saida}")
    print(f"Quantidade de ORFs virais filtrados: {len(banco_saida)}")

def tabela_para_fasta(caminho_tabela, caminho_fasta, nome_base):
    """
    Converte uma tabela em formato Excel para um arquivo FASTA.
    """
    tabela = pd.read_excel(caminho_tabela, header=None)
    registros = []

    for _, linha in tabela.iterrows():
        identificador = linha[0]
        sequencia = linha[16]
        registros.append(SeqRecord(Seq(sequencia), id=str(identificador), description=""))

    SeqIO.write(registros, caminho_fasta, "fasta")
    print(f"FASTA gerado: {caminho_fasta}")

def executar_cdhit(caminho_fasta, nome_base):
    """
    Executa o CD-HIT para clusterizar sequências e reduzir redundância.
    """
    saida_cdhit = f"{nome_base}_cdhit.fasta"
    comando = [
        "cd-hit-est", "-i", caminho_fasta, "-o", saida_cdhit, "-c", "0.9", "-n", "5",
        "-M", str(memoria), "-d", "0", "-T", str(threads)
    ]
    subprocess.run(comando)
    print(f"CD-HIT concluído. Saída: {saida_cdhit}")
    return saida_cdhit

def fasta_para_tabela(caminho_fasta, caminho_tabela, nome_base):
    """
    Converte um arquivo FASTA para uma tabela usando DIAMOND.
    """
    comando = [
        "diamond", "blastx", "--query", caminho_fasta, "--db", caminho_db_diamond,
        "--out", caminho_tabela, "--outfmt", "6",
        "qseqid", "sseqid", "qlen", "slen", "pident", "length", "mismatch", "gapopen",
        "qstart", "qend", "sstart", "send", "evalue", "bitscore", "stitle", "qtitle", "full_qseq",
        "--max-target-seqs", "1", "--threads", str(threads)
    ]
    subprocess.run(comando)
    print(f"DIAMOND concluído. Saída: {caminho_tabela}")

def filtrar_proteinas(caminho_tabela, nome_base):
    """
    Filtra hits com base em proteínas de interesse.
    """
    proteinas_interesse = re.compile(
        r"RdRp|RNA-dependent RNA polymerase|hypothetical protein|ORF|capsid|coat|replicase|glycoprotein|nucleoprotein|nucleocapsid"
    )

    tabela = pd.read_csv(caminho_tabela, sep="\t", header=None)
    tabela_filtrada = tabela[tabela[14].str.contains(proteinas_interesse, na=False)]

    caminho_saida = f"{nome_base}_proteins_filtered.tabular"
    tabela_filtrada.to_csv(caminho_saida, sep="\t", index=False, header=False)
    print(f"Tabela filtrada por proteínas de interesse salva como: {caminho_saida}")
    return caminho_saida

if __name__ == "__main__":
    try:
        nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]

        # 1. Filtrar melhores hits
        extracao(caminho_arquivo, nome_base)

        # 2. Converter para FASTA
        caminho_fasta = f"{nome_base}_hitfiltered.fasta"
        tabela_para_fasta(f"{nome_base}_hitfiltered.xlsx", caminho_fasta, nome_base)

        # 3. Executar CD-HIT
        saida_cdhit = executar_cdhit(caminho_fasta, nome_base)

        # 4. Converter de volta para tabela
        caminho_tabela_diamond = saida_cdhit.replace('.fasta', '_diamond.tabular')
        fasta_para_tabela(saida_cdhit, caminho_tabela_diamond, nome_base)

        # 5. Filtrar por proteínas de interesse
        caminho_proteins_filtered = filtrar_proteinas(caminho_tabela_diamond, nome_base)

        # 6. Identificar táxons
        identificar_taxons(caminho_proteins_filtered, nome_base)

    except Exception as e:
        print(f"Erro na execução: {e}")
