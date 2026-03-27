import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_csv("c:\\Users\\Administrator\\Desktop\\dfnova_tabela.csv")

# Plotar o heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.set_index('vias').dropna(), cmap='coolwarm', square=True, cbar=False)
plt.title('Heatmap de Bolhas')
plt.xlabel('Variável')
plt.ylabel('Vias')

# Adicionar bolhas
for i, row in df.iterrows():
    for j, value in enumerate(row[1:]):
        if pd.notnull(value):
            plt.scatter(j + 0.5, i + 0.5, s=value*100, color='black', alpha=0.7)

plt.xticks(rotation=90)
plt.yticks(ticks=range(len(df)), labels=df['vias'])
plt.tight_layout()
plt.show()
