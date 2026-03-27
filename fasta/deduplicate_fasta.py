from Bio import SeqIO
import sys

def remove_duplicates(input_fasta, output_fasta):
    seen = set()
    unique_sequences = []

    # Leitura do arquivo FASTA de entrada
    for record in SeqIO.parse(input_fasta, "fasta"):
        if record.id not in seen:
            seen.add(record.id)
            unique_sequences.append(record)

    # Escrita do arquivo FASTA de saída sem duplicatas
    SeqIO.write(unique_sequences, output_fasta, "fasta")
    print(f"Arquivo FASTA sem duplicatas foi salvo em: {output_fasta}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python remove_duplicates.py <input_fasta> <output_fasta>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    remove_duplicates(input_fasta, output_fasta)
