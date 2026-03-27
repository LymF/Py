import os
import re
from Bio import SeqIO
import subprocess

# Definir caminho de trabalho
working_dir = "/home/lucas/laiana"

# Abrir arquivo EVEs
with open(os.path.join(working_dir, "evesadapted.txt"), "r") as f:
    eves = f.readlines()

# Função para extrair elementos do arquivo gff3
def extract_flanking_regions(gff3_file, scaffold, start, end, output_gff):
    with open(gff3_file, "r") as gff, open(output_gff, "w") as out_gff:
        for line in gff:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if len(fields) < 9:
                continue
            feature_scaffold = fields[0]
            feature_start = int(fields[3])
            feature_end = int(fields[4])
            # Verificar se está no scaffold correto e na faixa de coordenadas
            if feature_scaffold == scaffold and ((feature_start >= start and feature_start <= end) or (feature_end >= start and feature_end <= end)):
                out_gff.write(line)

# Processar cada EVE
for eve in eves:
    if eve.startswith(">"):
        # Exemplo: >Ceratocystis_smalleyi_CMW14800[51322 - 52527]_scaffold_114 
        match = re.match(r">(.+)\[(\d+) - (\d+)\]_scaffold_(\S+)", eve)
        if not match:
            continue
        species = match.group(1)
        start_coord = int(match.group(2))
        end_coord = int(match.group(3))
        scaffold = f"scaffold_{match.group(4)}"

        # Definir regiões flanqueadoras
        flanking_start = max(0, start_coord - 10000)  # Evitar coordenadas negativas
        flanking_end = end_coord + 10000

        # Acessar o arquivo gff3
        gff3_dir = os.path.join(working_dir, species)
        gff3_file = os.path.join(gff3_dir, f"{species}.gff3")
        if not os.path.exists(gff3_file):
            print(f"Arquivo {gff3_file} não encontrado. Pulando...")
            continue

        # Criar arquivo de saída gff para regiões flanqueadoras
        output_gff = os.path.join(working_dir, f"{species}_flanking_{scaffold}.gff3")
        extract_flanking_regions(gff3_file, scaffold, flanking_start, flanking_end, output_gff)

        # Usar bedtools para extrair as sequências das regiões flanqueadoras
        genome_fasta = os.path.join(gff3_dir, f"{species}.scaffolds.fa")
        flanking_fasta = os.path.join(working_dir, f"{species}_flanking_sequences_{scaffold}.fasta")
        
        # Bedtools getfasta
        bedtools_command = [
            "bedtools", "getfasta",
            "-fi", genome_fasta,
            "-bed", output_gff,
            "-fo", flanking_fasta,
            "-name"
        ]
        
        try:
            subprocess.run(bedtools_command, check=True)
        except Exception as e:
            print(f"Erro ao executar bedtools: {e}")
            continue
        
        # Extrair sequência da EVE
        eve_sequence = ""
        is_eve_sequence = False
        for line in eves:
            if line.startswith(eve.strip()):
                is_eve_sequence = True
                continue
            if is_eve_sequence:
                if line.startswith(">"):
                    break
                eve_sequence += line.strip()

        # Extrair sequência completa do intervalo flanqueador
        complete_flanking_sequence = ""
        for record in SeqIO.parse(genome_fasta, "fasta"):
            if record.id == scaffold:
                complete_flanking_sequence = str(record.seq[flanking_start:flanking_end])
                break

        # Combinar sequência completa do intervalo flanqueador com a EVE
        combined_sequence = (
            complete_flanking_sequence[:10000]  # Região inicial
            + eve_sequence                     # Sequência da EVE
            + complete_flanking_sequence[-10000:]  # Região final
        )

        # Criar arquivo final com a sequência combinada
        combined_fasta = os.path.join(working_dir, f"{species}_merged_flanking_with_EVE_{scaffold}.fasta")
        with open(combined_fasta, "w") as combined_out:
            combined_out.write(f">Combined_{species}_flanking_with_EVE_{scaffold}\n{combined_sequence}\n")

print("Análise concluída!")
