def count_reads_in_fastq(fastq_file):
    """
    Conta o número de reads em um arquivo FASTQ.
    
    Args:
        fastq_file (str): Caminho para o arquivo FASTQ.
    
    Returns:
        int: Número total de reads no arquivo.
    """
    try:
        with open(fastq_file, 'r') as file:
            total_lines = sum(1 for _ in file)
        # Cada read ocupa 4 linhas
        total_reads = total_lines // 4
        return total_reads
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None

# Exemplo de uso
fastq_path = "/home/lucas/Documents/papers/srnas-fungi/Ac2012_1_1.fq"
reads_count = count_reads_in_fastq(fastq_path)
if reads_count is not None:
    print(f"O arquivo {fastq_path} contém {reads_count} reads.")
