import os
import csv
import time
import requests
from dotenv import load_dotenv

def extrair_timeline_geral():
    load_dotenv()
    usuario = os.getenv('BSKY_USER')
    senha   = os.getenv('BSKY_PW')

    BASE_URL = "https://bsky.social/xrpc"
    SESSION_URL = f"{BASE_URL}/com.atproto.server.createSession"
    FEED_URL = f"{BASE_URL}/app.bsky.feed.getAuthorFeed"

    print("📡 Autenticando na API do Bluesky...")
    try:
        resp_auth = requests.post(SESSION_URL, json={"identifier": usuario, "password": senha})
        resp_auth.raise_for_status()
        token = resp_auth.json()["accessJwt"]
        print("📡 Login realizado com sucesso!")
    except Exception as e:
        print(f"❌ Falha na autenticação: {e}")
        return

    HEADERS = {"Authorization": f"Bearer {token}"}

    # Lista completa e corrigida com os 5 de cada comunidade
    perfis_alvo = [
        # Comunidade 4 (Nicho TCG e Comercial)
        "amalgamcorps.bsky.social",
        "pokejungle.bsky.social",
        "sushibunniii.bsky.social",
        "memecchisu.bsky.social",
        "toinelay.bsky.social",
        
        # Comunidade 2 (Discussão Geral, Jogos e Arte) - AGORA COM OS 5 CORRETOS
        "melynart.bsky.social",
        "ikuvaito.bsky.social",
        "rotomamiti.bsky.social",
        # (pokejungle e sushibunniii já estão inclusos acima, o Python limpa duplicados se houver, 
        # mas mantive a ordem lógica para a API varrer)
        
        # Comunidade 3 (Consumo de Mídia e Animação)
        "pkmnframes.bsky.social",
        "shadepiplup10.bsky.social",
        "mooncatte.bsky.social",
        "animejunkiesama.bsky.social",
        "billymaier.bsky.social",
        
        # Comunidade 1 (Engajamento e Interação de Fãs)
        "funranium.bsky.social",
        "merrickmonroe.com",
        "lavenderqueen420.bsky.social",
        "jens0331.bsky.social",
        "mikechenwriter.bsky.social"
    ]

    # Remove duplicatas mantendo a ordem para não fazer requisições repetidas à toa
    perfis_alvo = list(dict.fromkeys(perfis_alvo))

    limite_posts = 15
    nome_arquivo_saida = "timeline_perfis_selecionados.csv"

    print(f"🗂️ Atualizando arquivo de saída '{nome_arquivo_saida}' com POSTS GERAIS...")
    
    with open(nome_arquivo_saida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["usuario_handle", "data_post", "texto_bruto", "like_count"])

        for handle in perfis_alvo:
            print(f"\n🔍 Buscando os últimos {limite_posts} posts GERAIS de: {handle}...")
            
            params = {
                "actor": handle,
                "limit": 40
            }

            try:
                resp = requests.get(FEED_URL, headers=HEADERS, params=params, timeout=15)
                
                if resp.status_code == 404:
                    print(f"⚠️ Perfil {handle} inacessível.")
                    continue
                    
                resp.raise_for_status()
                dados = resp.json()
                feed = dados.get("feed", [])

                if not feed:
                    print(f"⚠️ Nenhuma publicação no perfil de {handle}.")
                    continue

                posts_salvos = 0
                for item in feed:
                    post = item.get("post", {})
                    record = post.get("record", {})
                    
                    autor_post = post.get("author", {}).get("handle", "")
                    if autor_post != handle:
                        continue
                        
                    texto = record.get("text", "")
                    data_post = record.get("createdAt", "")
                    like_count = post.get("likeCount", 0)

                    texto_linha = texto.replace("\n", " ").replace("\r", " ") if texto else "[Apenas Mídia/Sem Texto]"
                    
                    writer.writerow([handle, data_post, texto_linha, like_count])
                    posts_salvos += 1
                    
                    if posts_salvos >= limite_posts:
                        break

                print(f"💾 {posts_salvos} posts gerais extraídos para {handle}.")
                
            except Exception as e:
                print(f"❌ Falha no perfil {handle}: {e}")
            
            time.sleep(1)

    print(f"\n✨ Processamento finalizado! Os dados gerais estão salvos em '{nome_arquivo_saida}'.")

if __name__ == "__main__":
    extrair_timeline_geral()