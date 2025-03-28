from Bio import SeqIO

# Arquivo de entrada e saída
input_file = "C:\\Users\\Administrator\\Desktop\\dali\\mirnas-oldpipe.fasta"
output_file = "C:\\Users\\Administrator\\Desktop\\dali\\mirnas-oldpipe-revtrans.fasta"

with open(output_file, "w") as output:
    for record in SeqIO.parse(input_file, "fasta"):
        record.seq = record.seq.transcribe().back_transcribe()  # Converte U -> T
        SeqIO.write(record, output, "fasta")

print("Conversão concluída!")
