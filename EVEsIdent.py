import os
import subprocess

# Configurações: Definir caminhos dos arquivos e diretórios
INPUT_DIR = "/home/lucas/evepip/genomas"  # Caminho para o diretório contendo os arquivos de genoma
DB_PATH = "/home/lucas/evepip/viraldb.dmnd"  # Caminho para o banco de dados DIAMOND

# Configurações de recursos
THREADS = 10  # Número de threads para cd-hit e diamond
MEMORY = "10000"  # Memória para cd-hit em MB

def run_getorf(input_genome, output_dir):
    """Executa o getorf do EMBOSS para identificar ORFs."""
    genome_name = os.path.basename(input_genome).split(".")[0]
    output_file = os.path.join(output_dir, f"{genome_name}_orfs.fasta")
    cmd = [
        "getorf",
        "-sequence", input_genome,
        "-outseq", output_file,
        "-minsize", "100",
        "-maxsize", "6000",
        "-find", "3"
    ]
    subprocess.run(cmd, check=True)
    return output_file

def run_cd_hit(input_file, output_dir):
    """Executa o cd-hit para reduzir redundância."""
    genome_name = os.path.basename(input_file).split("_")[0]
    output_file = os.path.join(output_dir, f"{genome_name}_orfs_cd-hit.fasta")
    cmd = [
        "cd-hit-est",
        "-i", input_file,
        "-o", output_file,
        "-c", "0.9",
        "-n", "5",
        "-T", str(THREADS),  # Configurar threads
        "-M", MEMORY  # Configurar memória
    ]
    subprocess.run(cmd, check=True)
    return output_file

def run_diamond(input_file, output_dir, db_path):
    """Executa o DIAMOND BLASTX."""
    genome_name = os.path.basename(input_file).split("_")[0]
    output_file = os.path.join(output_dir, f"{genome_name}_blast.tsv")
    cmd = [
        "diamond", "blastx",
        "-d", db_path,
        "-q", input_file,
        "-o", output_file,
        "--max-target-seqs", "5",
        "--outfmt", "6",
        "qseqid", "sseqid", "qlen", "slen", "pident", "length",
        "mismatch", "gapopen", "qstart", "qend", "sstart", "send",
        "evalue", "bitscore", "stitle", "qtitle", "full_qseq",
        "--threads", str(THREADS)  # Configurar threads
    ]
    subprocess.run(cmd, check=True)
    return output_file

def process_genome(input_genome, db_path):
    """Executa o pipeline para um único genoma."""
    genome_name = os.path.basename(input_genome).split(".")[0]
    output_dir = f"{genome_name}_results"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Identificar ORFs com getorf
    print(f"Processando {genome_name}: Executando getorf...")
    orfs_file = run_getorf(input_genome, output_dir)

    # 2. Reduzir redundância com cd-hit
    print(f"Processando {genome_name}: Executando cd-hit...")
    cd_hit_file = run_cd_hit(orfs_file, output_dir)

    # 3. Alinhar com DIAMOND BLASTX
    print(f"Processando {genome_name}: Executando DIAMOND BLASTX...")
    run_diamond(cd_hit_file, output_dir, db_path)

    print(f"Análise concluída para {genome_name}! Resultados salvos em {output_dir}.")

def main(input_dir, db_path):
    """Pipeline principal para análise de EVEs em múltiplos arquivos."""
    for file in os.listdir(input_dir):
        if file.endswith(".fna") or file.endswith(".fasta"):
            input_genome = os.path.join(input_dir, file)
            process_genome(input_genome, db_path)

if __name__ == "__main__":
    main(INPUT_DIR, DB_PATH)
