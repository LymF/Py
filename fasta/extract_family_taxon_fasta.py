import argparse
from Bio import Entrez, SeqIO
import re
import time

# Configure seu e-mail para acessar a API do NCBI
Entrez.email = "jp.uesc17@gmail.com"

def get_taxonomy_from_ncbi(accession):
    """
    Consulta o NCBI para obter a família taxonômica de uma proteína a partir do ID de acesso.
    """
    try:
        print(f"🔍 Buscando taxonomia para: {accession}...")
        handle = Entrez.esearch(db="protein", term=accession, retmode="xml")
        search_results = Entrez.read(handle)
        handle.close()
        
        if not search_results["IdList"]:
            print(f"⚠️ Nenhum resultado encontrado para {accession}, marcado como 'Unknown_Family'")
            return "Unknown_Family"
        
        protein_id = search_results["IdList"][0]
        handle = Entrez.efetch(db="protein", id=protein_id, retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        # Obtém a taxonomia da resposta
        taxonomy = records[0]['GBSeq_taxonomy']
        taxon_list = taxonomy.split("; ")  # Divide os níveis taxonômicos
        
        # Encontra a família dentro da taxonomia
        for taxon in taxon_list:
            if "viridae" in taxon.lower():  # Filtra termos que indicam família viral
                print(f"✅ Família identificada: {taxon}")
                return taxon
        
        print("⚠️ Família não encontrada, marcado como 'Unknown_Family'")
        return "Unknown_Family"
    
    except Exception as e:
        print(f"❌ Erro ao consultar {accession}: {e}")
        return "Unknown_Family"

def process_fasta(input_fasta, output_fasta):
    """
    Lê um arquivo FASTA, obtém a família para cada sequência e salva um novo FASTA com o nome atualizado.
    """
    with open(input_fasta, "r") as fasta_file, open(output_fasta, "w") as output_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            match = re.match(r"([A-Za-z0-9_]+\.?[0-9]*)", record.id)  # Captura IDs como YP_009507925.1 ou XJP19702.1
            if not match:
                print(f"⚠️ ID inválido ignorado: {record.id}")
                continue
            
            accession = match.group(1)  # Pega o ID de acesso correto
            family = get_taxonomy_from_ncbi(accession)
            
            # Adiciona a família ao final do header com "-" ao invés de "|"
            record.id = f"{record.id}-{family.replace(' ', '_')}"
            record.description = ""  # Remove descrição extra
            
            SeqIO.write(record, output_file, "fasta")
            time.sleep(0.5)  # Pequeno atraso para evitar sobrecarga na API do NCBI

    print(f"\n✅ Arquivo processado salvo como {output_fasta}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adiciona a família ao final dos headers no FASTA.")
    parser.add_argument("-i", "--input", required=True, help="Arquivo de entrada (FASTA ou TXT).")
    parser.add_argument("-o", "--output", required=True, help="Arquivo de saída (FASTA).")

    args = parser.parse_args()
    process_fasta(args.input, args.output)
