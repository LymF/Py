from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio.Blast import NCBIXML
import os

def run_blastn(input_fasta, output_tabular, database="nt", program="blastn"):
    """
    Executa uma pesquisa blastn online usando o NCBI BLAST.

    :param input_fasta: Caminho para o arquivo FASTA de entrada.
    :param output_tabular: Nome do arquivo de saída tabular para os resultados BLAST.
    :param database: Nome do banco de dados BLAST (padrão: "nr").
    :param program: Programa BLAST a ser usado (padrão: "blastn").
    """
    # Verificar se o arquivo FASTA de entrada existe
    if not os.path.exists(input_fasta):
        print(f"Arquivo {input_fasta} não encontrado.")
        return

    # Extrair o diretório do caminho do arquivo de entrada
    input_dir = os.path.dirname(input_fasta)

    # Ler todas as sequências do arquivo FASTA
    records = list(SeqIO.parse(input_fasta, "fasta"))

    # Verificar se há pelo menos uma sequência no arquivo
    if not records:
        print("Nenhuma sequência encontrada no arquivo FASTA.")
        return

    print(f"Total de {len(records)} sequências encontradas no arquivo FASTA.")

    # Construir o caminho do arquivo de saída no mesmo diretório do arquivo de entrada
    output_tabular = os.path.join(input_dir, output_tabular)

    # Abrir o arquivo de saída tabular
    with open(output_tabular, "w") as output_file:
        # Escrever o cabeçalho no arquivo de saída
        output_file.write("qseqid\tsseqid\tqlen\tslen\tpident\tevalue\tbitscore\tstitle\tfull_qseq\n")

        # Iterar sobre todas as sequências no arquivo FASTA
        for i, record in enumerate(records, start=1):
            print(f"Executando blastn para sequência {i} de {len(records)}")

            # Executar a pesquisa blastn online para cada sequência
            try:
                result_handle = NCBIWWW.qblast(program, database, record.seq, format_type='TextType')

                # Ler o conteúdo do resultado
                result_content = result_handle.read()

                # Verificar se a resposta está em formato XML
                if result_content.startswith(b'<?xml'):
                    result_content_str = result_content.decode()  # Converter bytes para string
                    blast_records = NCBIXML.read(result_content_str)
                    for alignment in blast_records.alignments:
                        hsp = alignment.hsps[0]
                        output_file.write(
                            f"{record.id}\t{alignment.hit_id}\t{blast_records.query_length}\t{alignment.length}\t"
                            f"{hsp.identities / hsp.align_length * 100:.2f}\t{hsp.expect}\t{hsp.bits}\t{alignment.title}\t{hsp.query}\n"
                        )
                else:
                    # Se não estiver em formato XML, assume-se que está em formato de texto
                    output_file.write(result_content.decode())  # Adicionei o .decode() para lidar com bytes
            except Exception as e:
                print(f"Erro ao executar blastn para a sequência {i}: {e}")

    print(f"Análise de blastn concluída. Resultado salvo em {output_tabular}")

if __name__ == "__main__":
    # Caminho para o arquivo FASTA de entrada
    input_fasta = "C:\\Users\\Lucas Melo\\Downloads\\teste\\SRR9041613_filtered.cdhit.fasta"

    # Nome para o arquivo de saída tabular
    output_tabular = "resultado_blastn.tabular"

    # Executar a pesquisa blastn para todas as sequências no arquivo FASTA
    run_blastn(input_fasta, output_tabular)
