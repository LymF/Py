import os
import glob

# Diretório onde os arquivos estão localizados
directory = 'C:\\Users\\Administrator\\Desktop\\Anderson\\sequences'

# Mude para o diretório especificado
os.chdir(directory)

# Encontrar todos os arquivos de contigs e singlets
contig_files = glob.glob('*.cap.contigs')
singlet_files = glob.glob('*.cap.singlets')

# Agrupar arquivos por biblioteca
libraries = {}
for file in contig_files + singlet_files:
    library_name = file.split('.fasta')[0]
    if library_name not in libraries:
        libraries[library_name] = {'contigs': [], 'singlets': []}
    if file.endswith('.cap.contigs'):
        libraries[library_name]['contigs'].append(file)
    elif file.endswith('.cap.singlets'):
        libraries[library_name]['singlets'].append(file)

# Criar arquivo de saída para cada biblioteca
for library_name, files in libraries.items():
    output_filename = f'{library_name}_contigs&singlets.fasta'
    with open(output_filename, 'w') as outfile:
        # Escrever contigs no arquivo de saída
        for contig_file in files['contigs']:
            with open(contig_file, 'r') as infile:
                outfile.write(infile.read())
        # Escrever singlets no arquivo de saída
        for singlet_file in files['singlets']:
            with open(singlet_file, 'r') as infile:
                outfile.write(infile.read())

    print(f'Arquivo de saída criado: {output_filename}')
