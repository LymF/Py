

def remover_duplicadas(arquivo_fasta):
  """
  Remove sequências duplicadas com base em cabeçalhos iguais em um arquivo FASTA.

  Args:
    arquivo_fasta: Caminho para o arquivo FASTA.

  Returns:
    Dicionário com as sequências únicas como chaves e seus cabeçalhos como valores.
  """

  sequencias_unicas = {}
  with open(arquivo_fasta, 'r') as f:
    for linha in f:
      if linha.startswith('>'):
        cabecalho = linha.strip()
        if cabecalho not in sequencias_unicas:
          sequencias_unicas[cabecalho] = []
      else:
        sequencia = linha.strip()
        sequencias_unicas[cabecalho].append(sequencia)

  # Mantém apenas a primeira sequência para cada header
  for cabecalho, sequencias in sequencias_unicas.items():
    sequencias_unicas[cabecalho] = sequencias[0]

  return sequencias_unicas


# Exemplo de uso
arquivo_fasta = 'c:\\Users\\Administrator\\Desktop\\Anderson\\\Transcriptoma_sem_duplicatas.fasta'
sequencias_unicas = remover_duplicadas(arquivo_fasta)

# Gravar as sequências únicas em um novo arquivo FASTA
with open('c:\\Users\\Administrator\\Desktop\\Anderson\\Transcriptoma_sem_duplicatas1.fasta', 'w') as f:
  for cabecalho, sequencia in sequencias_unicas.items():
    f.write(cabecalho + '\n')
    f.write(sequencia + '\n')
