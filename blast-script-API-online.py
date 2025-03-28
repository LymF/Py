import argparse
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
import csv
from concurrent.futures import ThreadPoolExecutor

# Função para calcular a cobertura
def calculate_coverage(query_length, alignment_length):
    return (alignment_length / query_length) * 100

# Função para executar o BLAST e salvar os resultados
def run_blast_and_save(seq_record, program, database, output_csv):
    query_id = seq_record.id
    query_sequence = str(seq_record.seq)
    query_length = len(seq_record.seq)

    print(f"Running {program} for: {query_id}")

    # Rodando o BLAST online
    result_handle = NCBIWWW.qblast(program, database, query_sequence)

    # Parseando os resultados
    blast_records = NCBIXML.parse(result_handle)

    rows = []
    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                # Calculando a identidade e cobertura
                per_identity = (hsp.identities / hsp.align_length) * 100
                coverage = calculate_coverage(query_length, hsp.align_length)

                # Extraindo o accession e o título do hit
                subject_id = alignment.hit_id
                subject_title = alignment.title
                accession = alignment.accession

                # Adicionando a linha ao resultado
                rows.append([query_id, subject_id, subject_title, hsp.expect, per_identity, coverage, accession, query_sequence])

    # Fechando o handle após o uso
    result_handle.close()

    # Salvando no CSV
    with open(output_csv, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)

# Função para configurar os argumentos da linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run BLAST searches and save results in CSV format.")
    parser.add_argument("input_fasta", help="Path to the input FASTA file.")
    parser.add_argument("output_dir", help="Directory where the output files will be saved.")
    parser.add_argument("prefix", help="Prefix for the output CSV files.")
    
    return parser.parse_args()

# Função principal
def main():
    # Parse dos argumentos
    args = parse_arguments()

    input_fasta = args.input_fasta
    output_dir = args.output_dir
    prefix = args.prefix

    # Parâmetros do BLAST
    blast_configs = [
        {"program": "blastn", "database": "nt", "output_csv": f"{output_dir}/{prefix}_blastn_results.csv"},
        {"program": "blastx", "database": "nr", "output_csv": f"{output_dir}/{prefix}_blastx_results.csv"},
    ]

    # Abrindo o arquivo multifasta
    with open(input_fasta, "r") as fasta_file:
        fasta_sequences = list(SeqIO.parse(fasta_file, "fasta"))

    # Iterando sobre as configurações de BLAST
    for config in blast_configs:
        program = config["program"]
        database = config["database"]
        output_csv = config["output_csv"]

        print(f"Running {program} for all sequences...")

        # Criando o arquivo de saída e escrevendo o cabeçalho
        with open(output_csv, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["query_id", "subject_id", "subject_title", "evalue", "per_identity", "coverage", "accession", "query_sequence"])

        # Usando ThreadPoolExecutor para paralelizar as requisições BLAST
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(run_blast_and_save, seq_record, program, database, output_csv)
                for seq_record in fasta_sequences
            ]

            # Aguardando todas as threads concluírem
            for future in futures:
                future.result()

        print(f"{program} completed. Results saved in {output_csv}.")

if __name__ == "__main__":
    main()
