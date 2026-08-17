import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import calinski_harabasz_score

# 1. Carrega diretamente o dataset normalizado que já existe na sua pasta
print("⏳ Carregando dataset normalizado...")
try:
    df_norm = pd.read_csv("dataset_pokemon_normalizado.csv")
except FileNotFoundError:
    print("❌ Erro: O arquivo 'dataset_pokemon_normalizado.csv' não foi encontrado na pasta.")
    exit()

atributos = ["frequencia_posts", "engajamento_medio", "tamanho_medio_texto", "taxa_midia", "uso_medio_hashtags"]
X = df_norm[atributos]

# 2. Execução da curva do Índice Calinski-Harabasz (CH)
valores_ch = []
K_range = list(range(2, 11))

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    score_ch = calinski_harabasz_score(X, labels)
    valores_ch.append(score_ch)

plt.figure(figsize=(8, 5))
plt.plot(K_range, valores_ch, 'ro-', linewidth=2)
plt.xlabel('Número de Clusters (K)')
plt.ylabel('Índice Calinski-Harabasz (CH)')
plt.title('Validação de Agrupamento: Índice Calinski-Harabasz')
plt.xticks(K_range)
plt.grid(True)
plt.tight_layout()
plt.savefig("validacao_calinski_harabasz.png")
plt.close()

# Identificar a melhor configuração de agrupamento
valores_ch = np.array(valores_ch)
indices_ordenados = np.argsort(valores_ch)[::-1] 

melhor_idx = indices_ordenados[0]
K_campeao = K_range[melhor_idx]
score_campeao = valores_ch[melhor_idx]

ks_para_gerar = [K_campeao]

segundo_idx = indices_ordenados[1]
K_segundo = K_range[segundo_idx]
score_segundo = valores_ch[segundo_idx]

if (score_segundo / score_campeao) >= 0.95:
    print(f"📊 Configurações potenciais: Principal K={K_campeao} ({score_campeao:.2f}) | Secundário K={K_segundo} ({score_segundo:.2f})")
    ks_para_gerar.append(K_segundo)
else:
    print(f"🎯 Configuração ideal identificada: K={K_campeao} ({score_campeao:.2f})")

# 3. Redução de dimensionalidade via PCA para projeção espacial
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X)
df_norm['pca_1'] = X_pca[:, 0]
df_norm['pca_2'] = X_pca[:, 1]

for k in ks_para_gerar:
    print(f"\n--- 🏗️ Gerando Estruturas para K = {k} ---")
    
    kmeans_final = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_resultado = kmeans_final.fit_predict(X)
    
    df_norm['cluster'] = labels_resultado
    
    # Projeção gráfica bidimensional dos clusters
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        x='pca_1', y='pca_2',
        hue='cluster',
        palette='Set1',
        data=df_norm,
        alpha=0.7,
        edgecolor='k'
    )
    plt.title(f'Projeção 2D dos Clusters de Usuários (PCA - K={k})')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.legend(title='Clusters')
    plt.tight_layout()
    
    nome_grafico = f"clusters_pokemon_k{k}.png"
    plt.savefig(nome_grafico)
    plt.close()
    print(f"🖼️ Gráfico '{nome_grafico}' gerado!")
    
    # Exibição do perfil estatístico médio dos clusters
    print("\n📈 Perfil Estatístico Médio dos Clusters (Valores Normalizados):")
    perfil_clusters = df_norm.groupby('cluster')[atributos].mean()
    perfil_clusters['quantidade_usuarios'] = df_norm.groupby('cluster').size()
    print(perfil_clusters.to_string())
    
    if k == K_campeao:
        # Grava o mapeamento consolidado associando o identificador ao cluster numérico correspondente
        df_saida = df_norm[['usuario_handle', 'cluster']].copy()
        
        # Reconstrói uma aproximação do engajamento original para servir de critério de ordenação no próximo script
        df_saida['engajamento_medio'] = df_norm['engajamento_medio']
        df_saida['frequencia_posts'] = df_norm['frequencia_posts']
        df_saida['tamanho_medio_texto'] = df_norm['tamanho_medio_texto']
        df_saida['taxa_midia'] = df_norm['taxa_midia']
        
        df_saida.to_csv("dataset_pokemon_minerado.csv", index=False)
        print("💾 Arquivo 'dataset_pokemon_minerado.csv' gerado com sucesso!")