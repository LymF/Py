import re
import sys
import pandas as pd
from Bio import Entrez
from time import sleep

Entrez.email = 'jp.uesc17@gmail.com'
test_planilha = pd.read_csv("C:/Users/Administrator/Desktop/Filtrar seqs diamond/sequences.csv")
test_planilha.drop_duplicates(subset="Organism_Name")
preproduction = pd.read_csv("C:/Users/Administrator/Desktop/Filtrar seqs diamond/planilha virfam - Página12.csv", header=None)
Entrez.api_key = 'ee7ccfdfa22559163c2bd8f3c822157ae108'
local_virus = "C:/Users/Administrator/Desktop/Filtrar seqs diamond/ICTV_Master_Species_List_2022_MSL38.v2.xlsx"
lt_ICTV = pd.read_excel(local_virus, sheet_name='MSL')
coluna_familia = lt_ICTV['Family']
coluna_genoma = lt_ICTV['Genome Composition']

data = {}
data_genome = {}
def get_ncbi_tax(taxon):
    print("rodando : "+taxon)
    try:
        '''Get in NCBI taxonomy'''
        # If the input is a string$
        if not re.match(r'\d+', taxon):
            # Get taxonomy ID using Entrez
            taxon2 = '"' + taxon + '"'
            handle = Entrez.esearch(
                db='taxonomy', term=taxon2, rettype='gb', retmode='text')
            record = Entrez.read(handle, validate=False)
            handle.close()
            sleep(0.2)
            # If there's no result
            if not record['IdList']:
                    tax_id = str(input("Qual o código ID de {}?\n".format(taxon)))

            tax_id = record['IdList']
        else:
            tax_id = taxon

        handle2 = Entrez.efetch(db='taxonomy', id=tax_id, retmode='xml')
        record2 = Entrez.read(handle2, validate=False)
        handle2.close()
        sleep(0.2)
        tax_list = record2[0]['LineageEx']

        valor = 0
        atualiza = 0
        apresenta = []
        for tax_element in range(len(tax_list)):
            if tax_list[tax_element]['Rank'] == 'family':
                apresenta.append(tax_list[tax_element]['ScientificName'])
                valor += 1
            elif (tax_list[tax_element]['Rank'] == 'no rank' or 'unclassified' in tax_list[tax_element]['ScientificName']) and valor == atualiza:
                apresenta.append(tax_list[tax_element]['ScientificName'])
                valor += 1
                atualiza += 1
            elif valor == 0 and tax_element == len(tax_list) - 1:
                apresenta.append(tax_list[tax_element]['ScientificName'])
                sleep(0.2)
        return apresenta[-1]
    except:
        sleep(60)
        get_ncbi_tax(taxon)


def busca_familia():
    global data
    global coluna_familia
    global coluna_genoma

    Caminho = str(input('Qual o caminho ?'))
    Caminho = Caminho.replace("\\", "/")
    Caminho = Caminho.replace("\"", "")
    Arquivo = str(input('Qual o nome do seu trabalho com .xlsx?'))
    lista_esp = []
    lista_analisada=[]
    lista_adict =[]
    lista_adct2=[]
    #Mudar de acordo com o tipo de input
    #Tabela = pd.read_table(Caminho, header=None, sep="\t")
    Tabela = pd.read_excel(Caminho, header=None)

#Mudar o numero da coluna para a coluna do nome dos hits
    for especie in Tabela[14]:
        especie = re.findall(r'\[.*\]', especie)
        lista_esp.append(str(especie))

    for i in lista_esp:
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.replace("'", '')
        lista_analisada.append(i)

    for j in lista_analisada:
        if j in data:
            lista_adict.append(data[j])
        else:
            """
            if j in list(preproduction[0]):
                variavel = preproduction[2][list(preproduction[0]).index(str(j))]
                lista_adict.append(variavel)
                data[j] = variavel
            """
            if str(j) in list(test_planilha["Organism_Name"]):
                variavel = test_planilha["Molecule_type"][list(test_planilha["Organism_Name"]).index(str(j))]
                lista_adict.append(variavel)
                data[j] = variavel
            else:
                sleep(4)
                variavel = get_ncbi_tax(j)
                lista_adict.append(variavel)
                data[j] = variavel

    for j in lista_adict:
        if str(j) in data_genome:
            lista_adct2.append(data_genome[j])
        else:
            a=0
            for i in range(len(coluna_familia)):
                if str(coluna_familia[i]) == j:
                    data_genome[j] = coluna_genoma[i]
                    a -= 1
                else:
                    a += 1
                    if a == len(coluna_familia):
                        data_genome[j] = j
            lista_adct2.append(data_genome[j])


    Tabela['adicao']=lista_adict
    Tabela['material']=lista_adct2

    Tabela.to_excel(Arquivo, sheet_name='famílias')

    Repetir = str(input('Você deseja repetir a operação: s ou n'))
    if Repetir == 's':
        busca_familia()
    else:
        print('Bom trabalho!!!')

busca_familia()

# /Users/jpues/Downloads/ICTV_Master_Species_List_2021_v3.xlsx
# /Users/jpues/Downloads/Galaxy33-[Diamond_on_data_31_and_data_29].tabular
# "C:\Users\jpues\Downloads\uesc.xlsx
# Sheet
# NOME
# funesta1.xlsx
# /Users/jpues/Downloads/SRR26324980.tabular
#"C:\Users\jpues\Downloads\SRR26324997.tabular"