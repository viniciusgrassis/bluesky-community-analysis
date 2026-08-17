import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

nome_entrada = "dataset_pokemon_texto_processado.csv"

try:
    df = pd.read_csv(nome_entrada)
    df['texto_limpo'] = df['texto_limpo'].fillna("")
    df = df[df['texto_limpo'] != ""]
    print(f"🎯 Total de documentos válidos no corpus: {len(df)}")
except Exception as e:
    print(f"❌ Erro ao ler o arquivo processado: {e}")
    df = pd.DataFrame()

if len(df) > 0:
    limiar_corte = df['like_count'].quantile(0.70)
    
    if pd.isna(limiar_corte) or limiar_corte == 0:
        limiar_corte = 1
        
    print(f"📊 Limiar estatístico de corte (Likes >= {limiar_corte} representa Alto Engajamento)")
    
    df_alto_engaj = df[df['like_count'] >= limiar_corte]
    df_baixo_engaj = df[df['like_count'] < limiar_corte]
    
    print(f"🔥 Documentos na Classe Alto Engajamento: {len(df_alto_engaj)}")
    print(f"❄️ Documentos na Classe Baixo Engajamento: {len(df_baixo_engaj)}")
else:
    print("❌ O dataset está vazio. Impossível continuar a mineração.")
    df_alto_engaj = pd.DataFrame()
    df_baixo_engaj = pd.DataFrame()

n_topicos = 3 
n_palavras_chave = 10
sns.set_theme(style="whitegrid")

def minerar_e_plotar_classe(dataframe, titulo_classe, sufixo_salvamento):
    """
    Executa o pipeline metodológico completo (TF-IDF + LDA) de forma isolada
    para a classe de documentos parametrizada.
    """
    if len(dataframe) < n_topicos:
        print(f"⚠️ Amostra de '{titulo_classe}' muito reduzida para extração de tópicos.")
        return

    corpus = dataframe['texto_limpo'].tolist()

    vetorizador = TfidfVectorizer(max_features=1000, min_df=2, max_df=0.95)
    try:
        X_tfidf = vetorizador.fit_transform(corpus)
        nomes_atributos = vetorizador.get_feature_names_out()
    except Exception as vec_err:
        print(f"⚠️ Erro ao aplicar TF-IDF na classe '{titulo_classe}': {vec_err}")
        return

    lda = LatentDirichletAllocation(n_components=n_topicos, random_state=42, max_iter=15)
    lda.fit(X_tfidf)

    fig, axes = plt.subplots(1, n_topicos, figsize=(18, 5), sharex=False)

    for idx_topico, topico in enumerate(lda.components_):
        top_indices = topico.argsort()[:-n_palavras_chave - 1:-1]
        top_palavras = [nomes_atributos[i] for i in top_indices]
        pesos = [topico[i] for i in top_indices]
        
        df_plot = pd.DataFrame({'Palavra': top_palavras, 'Importância': pesos})
        
        ax = axes[idx_topico]
        sns.barplot(x='Importância', y='Palavra', data=df_plot, ax=ax, palette='viridis', hue='Palavra', legend=False)
        ax.set_title(f'Tópico Latente {idx_topico + 1}')
        ax.set_xlabel('Peso Probabilístico (LDA)')
        ax.set_ylabel('')

    plt.suptitle(f'Mineração de Texto Bluesky: Termos Dominantes - {titulo_classe}', fontsize=16, weight='bold')
    plt.tight_layout()

    nome_grafico = f"topicos_lda_{sufixo_salvamento}.png"
    plt.savefig(nome_grafico, dpi=300)
    plt.close()
    print(f"💾 Gráfico '{nome_grafico}' gerado e salvo com sucesso!")

    print(f"📝 Perfis resumidos - {titulo_classe}:")
    for idx_topico, topico in enumerate(lda.components_):
        top_indices = topico.argsort()[:-6:-1]
        termos = [nomes_atributos[i] for i in top_indices]
        print(f"  📌 Tópico {idx_topico + 1}: {', '.join(termos)}")
    print("-" * 50)

if len(df_alto_engaj) > 0:
    minerar_e_plotar_classe(df_alto_engaj, "Classe Alto Engajamento (Hubs/Influenciadores)", "alto_engajamento")
if len(df_baixo_engaj) > 0:
    minerar_e_plotar_classe(df_baixo_engaj, "Classe Baixo Engajamento (Usuários Casuais)", "baixo_engajamento")

print("\n🚀 Pipeline comparativo concluído de ponta a ponta!")