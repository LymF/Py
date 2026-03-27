from Bio import SeqIO

def split_fasta_to_kmers(input_fasta, output_fasta, kmer_size=2000):
    """
    Divide sequências de um arquivo FASTA em pedaços de tamanho fixo (kmers), 
    incluindo kmers incompletos no final.

    :param input_fasta: Caminho para o arquivo FASTA de entrada.
    :param output_fasta: Caminho para o arquivo FASTA de saída com os kmers.
    :param kmer_size: Tamanho de cada kmer. Default é 2000 bp.
    """
    with open(output_fasta, "w") as output_handle:
        for record in SeqIO.parse(input_fasta, "fasta"):
            sequence = str(record.seq)
            for i in range(0, len(sequence), kmer_size):
                kmer = sequence[i:i + kmer_size]
                kmer_id = f"{record.id}_kmer_{i+1}-{i+len(kmer)}"
                output_handle.write(f">{kmer_id}\n{kmer}\n")

# Exemplo de uso:
input_fasta = "C:\\Users\\Administrator\\Desktop\\dali\\qfasciata.fa"
output_fasta = "C:\\Users\\Administrator\\Desktop\\dali\\qfasc2kgenom.split.2Kmer.fa"
split_fasta_to_kmers(input_fasta, output_fasta, kmer_size=2000)
