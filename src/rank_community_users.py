import pandas as pd

def extrair_top_comunidades_por_engajamento():
    arquivo_processado = "dataset_pokemon_texto_processado.csv"
    arquivo_bruto = "dataset_pokemon_texto_bruto.csv"
    
    print("⏳ Carregando bases de dados do pipeline...")
    try:
        df_proc = pd.read_csv(arquivo_processado)
        df_bruto = pd.read_csv(arquivo_bruto)
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo não encontrado. Detalhes: {e}")
        return

    df_proc['usuario_handle'] = df_proc['usuario_handle'].astype(str).str.strip()
    df_bruto['usuario_handle'] = df_bruto['usuario_handle'].astype(str).str.strip()

    # Definição das comunidades baseada nos resultados do Louvain (analise_redes.py)
    comunidades_louvain = {
        "Comunidade 4 (Nicho TCG e Comercial)": [
            'tcg', 'new', 'pokemontcg', 'sale', 'seal', 'mega', 'card', 'look', 
            'amazon', 'box', 'booster', 'collect', 'discord', 'trainer', 'alert', 
            'restock', 'realtim', 'pack'
        ],
        "Comunidade 2 (Discussão Geral, Jogos e Arte)": [
            'game', 'like', 'one', 'art', 'get', 'artfight', 'play', 'make', 
            'want', 'time', 'switch', 'also'
        ],
        "Comunidade 3 (Consumo de Mídia e Animação)": [
            'episod', 'season', 'fire', 'ice', 'frame', 'timestamp', 'caption'
        ],
        "Comunidade 1 (Engajamento e Interação de Fãs)": [
            'answer', 'wrong', 'fav'
        ]
    }

    print(f"🎯 Filtrando e agregando impacto por Engajamento Total Acumulado (Opção A)...\n")

    for nome_comunidade, palavras_chave in comunidades_louvain.items():
        print("=" * 80)
        print(f"📊 ALGORITMO DE LOUVAIN: {nome_comunidade.upper()}")
        print("=" * 80)
        
        # Isola os posts que contêm os radicais da comunidade atual
        indices_comunidade = []
        for idx, row in df_proc.iterrows():
            texto = str(row['texto_limpo']).split()
            if any(termo in texto for termo in palavras_chave):
                indices_comunidade.append(idx)
                
        df_comunidade_posts = df_proc.iloc[indices_comunidade].copy()
        
        if len(df_comunidade_posts) == 0:
            print("⚠️ Nenhuma postagem correspondente mapeada para esta partição.")
            continue
            
        # Agrupamento e soma do engajamento (likes) por usuário dentro desta comunidade
        # Inclui a contagem de posts como critério secundário de desempate
        df_agrupado = df_comunidade_posts.groupby('usuario_handle').agg(
            engajamento_total=('like_count', 'sum'),
            total_posts_comunidade=('post_id', 'count')
        ).reset_index()
        
        # Ordenação Decrescente: Prioridade 1 = Likes Totais | Prioridade 2 = Volume de Posts
        df_ranking = df_agrupado.sort_values(
            by=['engajamento_total', 'total_posts_comunidade'], 
            ascending=[False, False]
        )
        
        # Captura os 5 primeiros handles após o corte estrito de impacto
        top_5_handles = df_ranking['usuario_handle'].head(5).tolist()
        
        for ranking, handle in enumerate(top_5_handles, 1):
            print(f"\n👤 [Top {ranking}] Usuário (Handle): {handle}")
            
            # Recupera as métricas calculadas para este perfil
            info_perfil = df_ranking[df_ranking['usuario_handle'] == handle].iloc[0]
            
            # Busca as postagens brutas originais deste usuário nesta comunidade
            posts_brutos_usuario = df_bruto[
                (df_bruto['usuario_handle'] == handle) & 
                (df_bruto['post_id'].isin(df_comunidade_posts['post_id']))
            ]
            
            print(f"   📈 Métricas na Comunidade -> Curtidas Acumuladas: {info_perfil['engajamento_total']} | Posts: {info_perfil['total_posts_comunidade']}")
            print(f"   📝 Linha do tempo de publicações coletadas:")
            
            for _, row_post in posts_brutos_usuario.head(5).iterrows():
                print(f"      - (Likes: {row_post['like_count']}) {row_post['texto_bruto']}")
            print("-" * 60)
        print("\n")

if __name__ == "__main__":
    extrair_top_comunidades_por_engajamento()