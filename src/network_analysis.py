import pandas as pd
import networkx as nx
import community as community_louvain  
import matplotlib.pyplot as plt
from collections import Counter
import itertools

nome_entrada = "dataset_pokemon_texto_processado.csv"
df = pd.read_csv(nome_entrada)
df['texto_limpo'] = df['texto_limpo'].fillna("")

documentos = [texto.split() for texto in df['texto_limpo'] if texto != ""]

print(f"📦 Construindo Rede de Coocorrência a partir de {len(documentos)} postagens...")

todas_palavras = list(itertools.chain(*documentos))
contagem_termos = Counter(todas_palavras)
termos_dominantes = [palavra for palavra, freq in contagem_termos.most_common(40)]

G = nx.Graph()

G.add_nodes_from(termos_dominantes)

combinacoes_arestas = Counter()
for doc in documentos:
    termos_filtrados = [termo for termo in doc if termo in termos_dominantes]
    termos_unicos = list(set(termos_filtrados))
    
    if len(termos_unicos) > 1:
        for u, v in itertools.combinations(sorted(termos_unicos), 2):
            combinacoes_arestas[(u, v)] += 1

for (u, v), peso in combinacoes_arestas.items():
    if peso >= 2: 
        G.add_edge(u, v, weight=peso)

print(f"📊 Topologia da Rede Gerada: {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")

particao = community_louvain.best_partition(G, weight='weight')
modularidade_q = community_louvain.modularity(particao, G, weight='weight')

print(f"✨ Comunidades detectadas pelo algoritmo de Louvain!")
print(f"📈 Coeficiente de Modularidade Obtido (Q): {modularidade_q:.4f}")

comunidades_dict = {}
for no, id_comunidade in particao.items():
    comunidades_dict.setdefault(id_comunidade, []).append(no)

print("\n📝 --- COMPOSIÇÃO TOPOLÓGICA DAS COMUNIDADES --- 📝")
for id_com, membros in comunidades_dict.items():
    print(f"👥 Comunidade {id_com + 1}: {', '.join(membros)}")
print("-" * 60)

plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G, k=0.4, seed=42)

cores_comunidades = [particao[no] for no in G.nodes()]

tamanhos_nos = [G.degree(no) * 120 for no in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_color=cores_comunidades, node_size=tamanhos_nos, cmap=plt.cm.tab10, alpha=0.9)
nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', width=[G[u][v]['weight'] * 0.3 for u, v in G.edges()])
nx.draw_networkx_labels(G, pos, font_size=11, font_weight='bold', font_color='black')

plt.title(f"Rede de Coocorrência de Termos (Bluesky - Pokémon)\nComunidades por Otimização de Modularidade (Louvain - Q = {modularidade_q:.3f})", fontsize=14, weight='bold')
plt.axis('off')
plt.tight_layout()

nome_grafico_rede = "comunidades_topologicas_rede.png"
plt.savefig(nome_grafico_rede, dpi=300)
plt.close()

print(f"💾 Gráfico de visualização espacial '{nome_grafico_rede}' salvo com sucesso!")