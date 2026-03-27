import os

from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO

def run_blastx_online_best_hit(input_file, output_file):
    # Obter o nome do arquivo sem extensão (SRRXXXX)
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Construir o nome do arquivo de saída com o sufixo "_blast_results.txt"
    output_file = os.path.join(os.path.dirname(input_file), f"{base_name}_blast_results.txt")

    # Ler as sequências do arquivo fasta
    sequences = list(SeqIO.parse(input_file, "fasta"))

    # Configurar e executar o BLASTX para cada sequência
    with open(output_file, "w") as out_handle:
        for i, seq_record in enumerate(sequences, start=1):
            print(f"Iniciando BLAST da sequência {i} de {len(sequences)}")
            result_handle = NCBIWWW.qblast("blastx", "nr", seq_record.seq, format_type="XML")

            # Analisar os resultados em formato XML
            blast_record = NCBIXML.read(result_handle)

            # Extrair informações do melhor hit
            if blast_record.alignments:
                best_hit = blast_record.alignments[0]
                hsp = best_hit.hsps[0]

                # Adicionar as colunas solicitadas
                qcovs = (hsp.query_end - hsp.query_start + 1) / len(seq_record) * 100
                qlen = len(seq_record)
                slen = best_hit.length

                # Salvar os resultados em um arquivo tabular
                out_handle.write(f"{seq_record.id}\t{hsp.identities / hsp.align_length * 100:.2f}%\t")
                out_handle.write("\t".join([
                    str(seq_record.id),
                    str(hsp.identities / hsp.align_length * 100),
                    str(best_hit.hit_id),
                    str(hsp.expect),
                    str(hsp.bits),
                    str(qlen),
                    str(slen),
                    str(best_hit.accession),
                    str(best_hit.title),
                    str(qcovs),
                ]))
                out_handle.write("\n")

    print("BLASTX online concluído. Melhores hits salvos em", output_file)

if __name__ == "__main__":
    # Substitua 'input.fasta' pelo caminho do seu arquivo fasta
    input_file = "C:\\Users\\Lucas Melo\\Downloads\\Daliane\\diamond\\filtrados\\novos\\fastateste.fasta"

    run_blastx_online_best_hit(input_file, None)  # None para usar o nome padrão de saída
