import pandas as pd

def has_exact_match(qseq, sseq, min_length=15):
    """Verifica se há pelo menos `min_length` nucleotídeos contíguos idênticos entre qseq e sseq."""
    for i in range(len(qseq) - min_length + 1):
        if qseq[i:i+min_length] == sseq[i:i+min_length]:
            return True
    return False

def process_blast_results(blast_file, output_file):
    columns = ["qseqid", "sseqid", "pident", "length", "mismatch", 
               "qstart", "qend", "sstart", "send", "qseq", "sseq"]
    
    df = pd.read_csv(blast_file, sep="\t", names=columns)
    
    # Adicionar uma nova coluna 'status' com 'positive' ou 'negative'
    df["status"] = df.apply(lambda row: "positive" if has_exact_match(row["qseq"], row["sseq"]) else "negative", axis=1)
    
    # Salvar o resultado com a nova coluna
    df.to_csv(output_file, sep="\t", index=False)
    print(f"Processamento concluído. Resultados salvos em {output_file}")

# Aplicar a função para os dois arquivos de BLAST
process_blast_results("/home/lucas/Documents/papers/bombus/blast/results_refseq.tsv", "/home/lucas/Documents/papers/bombus/blast/processed_results_refseq.tsv")
process_blast_results("/home/lucas/Documents/papers/bombus/blast/results_abelhas.tsv", "/home/lucas/Documents/papers/bombus/blast/processed_results_abelhas.tsv")
