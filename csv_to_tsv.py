import csv

def csv_to_tsv(input_csv_file, output_tsv_file):
    with open(input_csv_file, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(output_tsv_file, 'w', newline='') as tsv_file:
            tsv_writer = csv.writer(tsv_file, delimiter='\t')
            for row in csv_reader:
                tsv_writer.writerow(row)

# Substitua 'input.csv' pelo caminho do seu arquivo CSV e 'output.tsv' pelo caminho onde você deseja salvar o arquivo TSV.
csv_to_tsv('c:\\Users\\Administrator\\Desktop\\Ortogolos\\anotação.csv', 'c:\\Users\\Administrator\\Desktop\\Ortogolos\\anotação.tsv')