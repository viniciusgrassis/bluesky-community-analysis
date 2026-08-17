import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# dados obtidos são carregados
df = pd.read_csv("dataset_pokemon.csv")
print(f"📊 Dataset carregado original: {df.shape[0]} usuários e {df.shape[1]} colunas.\n")

# Pré processamento inicial dos dados, eliminando ruídos, valorez incompletos e etc.
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(subset=["frequencia_posts", "engajamento_medio", "tamanho_medio_texto", "taxa_midia", "uso_medio_hashtags"], inplace=True)
print(f"🧹 Após a limpeza de dados nulos/inconsistentes: {df.shape[0]} usuários restantes.\n")

# Cálculo de valores básicos: Mín, Máx, Média, Mediana, Desvio-Padrão
estatisticas = df.describe().T
estatisticas['mediana'] = df.median(numeric_only=True)

print("📈 --- ESTATÍSTICAS BÁSICAS DOS ATRIBUTOS --- 📈")
print(estatisticas[["min", "max", "mean", "mediana", "std"]].to_string())

# Geração de gráficos e histogramas para visualização
sns.set_theme(style="whitegrid")

atributos_analise = ["frequencia_posts", "engajamento_medio", "tamanho_medio_texto", "taxa_midia"]

plt.figure(figsize=(15, 10))
for i, col in enumerate(atributos_analise, 1):
    plt.subplot(2, 2, i)
    sns.histplot(df[col], kde=True, color="purple", bins=20)
    plt.title(f"Distribuição de {col}")
plt.tight_layout()
plt.savefig("distribuicao_histogramas.png")
plt.close()
print("\n🖼️ Gráfico 'distribuicao_histogramas.png' salvo com sucesso!")

# Box-plots ajudam a identificar outliers
plt.figure(figsize=(15, 10))
for i, col in enumerate(atributos_analise, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(y=df[col], color="skyblue")
    plt.title(f"Box-plot de {col}")
plt.tight_layout()
plt.savefig("analise_boxplots.png")
plt.close()
print("🖼️ Gráfico 'analise_boxplots.png' salvo com sucesso!")

# Análise para correlação de dados não rotulados
plt.figure(figsize=(8, 6))

# Calcula a matriz de correlação de Pearson
matriz_corr = df[atributos_analise + ["uso_medio_hashtags"]].corr()
sns.heatmap(matriz_corr, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
plt.title("Matriz de Correlação entre Atributos do Bluesky")
plt.tight_layout()
plt.savefig("matriz_correlacao.png")
plt.close()
print("🖼️ Gráfico 'matriz_correlacao.png' salvo com sucesso!")

# Normalização dos dados aplicandoa a fórmula (x - min) / (max - min) para cada atributo
df_normalizado = df.copy()
for col in atributos_analise + ["uso_medio_hashtags"]:
    min_val = df[col].min()
    max_val = df[col].max()
    if max_val != min_val:
        df_normalizado[col] = (df[col] - min_val) / (max_val - min_val)
    else:
        df_normalizado[col] = 0.0

# Por fim, o novo dataset é salvo
df_normalizado.to_csv("dataset_pokemon_normalizado.csv", index=False)
print("\n✨ Normalização Min-Max concluída!")
print("💾 Novo arquivo 'dataset_pokemon_normalizado.csv' gerado prontinho para a mineração.")