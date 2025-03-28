import openpyxl as op
import re
import pandas as pd
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
import subprocess

# Imprescindivel que o saida do diamond seja formatada assim: --outfmt '6' qseqid sseqid qlen slen pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle qtitle full_qseq
# Configuração de arquivos
caminho_arquivo_folder = "/home/lucas/evepip/diamonds/"  # Caminho da pasta onde os arquivos .tabular saídos do diamond estão
local_virus = "/home/lucas/evepip/ICTV_Master_Species_List_2022_MSL38.v2.xlsx"  # Substitua pelo caminho do arquivo ICTV
caminho_db_diamond = "/home/lucas/evepip/viraldb.dmnd"  # Substitua pelo caminho do banco de dados do DIAMOND
Entrez.email = 'jp.uesc17@gmail.com'
Entrez.api_key = 'ee7ccfdfa22559163c2bd8f3c822157ae108'

# Mudar de acordo com a máquina
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

def criar_pasta_saida(caminho_arquivo):
    """
    Cria uma pasta para armazenar os resultados. O nome da pasta será o nome do arquivo original com '_results' adicionado.
    """
    nome_arquivo = os.path.basename(caminho_arquivo).replace('.tabular', '')
    pasta_saida = os.path.join(os.path.dirname(caminho_arquivo), f"{nome_arquivo}_results")
    os.makedirs(pasta_saida, exist_ok=True)
    return pasta_saida

def identificar_taxons(caminho_tabela, output_folder, nome_arquivo):
    """
    Identifica os táxons usando o NCBI e o ICTV Master Species List.
    """
    lt_ICTV = pd.read_excel(local_virus, sheet_name='MSL')
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

    nome_saida = os.path.join(output_folder, f"{nome_arquivo}_taxons_identificados.xlsx")
    tabela.to_excel(nome_saida, index=False)
    print(f"Tabela com identificação de táxons salva como: {nome_saida}")
    return nome_saida

def extracao(caminho_arquivo, output_folder, nome_arquivo):
    """
    Processa a saída do DIAMOND para filtrar os melhores hits com base em e-value e bitscore.
    Salva os resultados em um arquivo Excel com sufixo '_hitfiltered'.
    """
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

    nome_saida = os.path.join(output_folder, f"{nome_arquivo}_hitfiltered.xlsx")
    book = op.Workbook()
    lista_page = book.active
    lista_page.title = "Filtered Hits"
    
    for linha in banco_saida:
        lista_page.append(linha)

    book.save(nome_saida)
    print(f"Arquivo salvo como: {nome_saida}")
    print(f"Quantidade de ORFs virais filtrados: {len(banco_saida)}")
    return nome_saida

def tabela_para_fasta(caminho_tabela, output_folder, nome_arquivo):
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

    caminho_fasta = os.path.join(output_folder, f"{nome_arquivo}_hitfiltered.fasta")
    SeqIO.write(registros, caminho_fasta, "fasta")
    print(f"FASTA gerado: {caminho_fasta}")
    return caminho_fasta

def executar_cdhit(caminho_fasta, output_folder, nome_arquivo):
    """
    Executa o CD-HIT para clusterizar sequências e reduzir redundância.
    """
    saida_cdhit = os.path.join(output_folder, f"{nome_arquivo}_cdhit_output.fasta")
    comando = [
        "cd-hit-est", "-i", caminho_fasta, "-o", saida_cdhit, "-c", "0.9", "-n", "5",
        "-M", str(memoria), "-d", "0", "-T", str(threads)
    ]
    subprocess.run(comando)
    print(f"CD-HIT concluído. Saída: {saida_cdhit}")
    return saida_cdhit

def fasta_para_tabela(caminho_fasta, output_folder, nome_arquivo):
    """
    Converte um arquivo FASTA para uma tabela usando DIAMOND.
    """
    caminho_tabela = os.path.join(output_folder, f"{nome_arquivo}_diamond_output.tabular")
    comando = [
        "diamond", "blastx", "--query", caminho_fasta, "--db", caminho_db_diamond,
        "--out", caminho_tabela, "--outfmt", "6",
        "qseqid", "sseqid", "qlen", "slen", "pident", "length", "mismatch", "gapopen",
        "qstart", "qend", "sstart", "send", "evalue", "bitscore", "stitle", "qtitle", "full_qseq",
        "--max-target-seqs", "1", "--threads", str(threads)
    ]
    subprocess.run(comando)
    print(f"DIAMOND concluído. Saída: {caminho_tabela}")
    return caminho_tabela

def filtrar_proteinas(caminho_tabela, output_folder, nome_arquivo):
    """
    Filtra hits com base em proteínas de interesse.
    """
    proteinas_interesse = re.compile(
        r"RdRp|RNA-dependent RNA polymerase|hypothetical protein|ORF|capsid|coat|replicase|glycoprotein|nucleoprotein|nucleocapsid"
    )

    tabela = pd.read_csv(caminho_tabela, sep="\t", header=None)
    tabela_filtrada = tabela[tabela[14].str.contains(proteinas_interesse, na=False)]  # Coluna 14 contém o título da sequência

    caminho_saida = os.path.join(output_folder, f"{nome_arquivo}_proteins_filtered.tabular")
    tabela_filtrada.to_csv(caminho_saida, sep="\t", header=False, index=False)
    print(f"Arquivo filtrado salvo como: {caminho_saida}")
    return caminho_saida

# Processar todos os arquivos .tabular
for arquivo in os.listdir(caminho_arquivo_folder):
    if arquivo.endswith(".tabular"):
        caminho_arquivo = os.path.join(caminho_arquivo_folder, arquivo)
        
        # Criar a pasta para o arquivo específico
        nome_arquivo = os.path.splitext(arquivo)[0]
        output_folder = criar_pasta_saida(caminho_arquivo)

        # Processar o arquivo na ordem correta
        print(f"Processando arquivo: {arquivo}")

        try:
            # 1. Filtrar melhores hits
            caminho_hitfiltered = extracao(caminho_arquivo, output_folder, nome_arquivo)

            # 2. Converter para FASTA
            caminho_fasta = tabela_para_fasta(caminho_hitfiltered, output_folder, nome_arquivo)

            # 3. Executar CD-HIT
            saida_cdhit = executar_cdhit(caminho_fasta, output_folder, nome_arquivo)

            # 4. Converter de volta para tabela
            caminho_tabela_diamond = fasta_para_tabela(saida_cdhit, output_folder, nome_arquivo)

            # 5. Filtrar por proteínas de interesse
            caminho_proteins_filtered = filtrar_proteinas(caminho_tabela_diamond, output_folder, nome_arquivo)

            # 6. Identificar táxons
            identificar_taxons(caminho_proteins_filtered, output_folder, nome_arquivo)

        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {e}")

print("Processamento concluído para todos os arquivos .tabular.")
