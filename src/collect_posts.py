import os
import csv
import time
import requests
from dotenv import load_dotenv


load_dotenv()
usuario = os.getenv('BSKY_USER')
senha   = os.getenv('BSKY_PW')


BASE_URL = "https://bsky.social/xrpc"
SEARCH_URL = f"{BASE_URL}/app.bsky.feed.searchPosts"
SESSION_URL = f"{BASE_URL}/com.atproto.server.createSession"

print("📡 Autenticando na API do Bluesky...")
resp_auth = requests.post(SESSION_URL, json={"identifier": usuario, "password": senha})
resp_auth.raise_for_status()
token = resp_auth.json()["accessJwt"]
display_name = resp_auth.json().get("handle", usuario)
print(f"📡 Login realizado com sucesso! Olá, {display_name}!")

HEADERS = {"Authorization": f"Bearer {token}"}

query = "Pokémon"
posts_desejados = 1000
limite_pagina = 50          
cursor = None
total_coletados = 0
ordenacao_atual = "latest"  
nome_arquivo = "dataset_pokemon_texto_bruto.csv"

print(f"🔍 Iniciando coleta massiva de textos sobre '{query}' (Meta: {posts_desejados} posts)...")

with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["post_id", "data_post", "usuario_handle", "texto_bruto", "like_count"])

    while total_coletados < posts_desejados:
        params = {
            "q":     query,
            "limit": limite_pagina,
            "sort":  ordenacao_atual,
        }
        if cursor:
            params["cursor"] = cursor

        try:
            resp = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=15)
            resp.raise_for_status()
            dados = resp.json()

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else None
            if status == 401:
                print("🔄 Token expirado, re-autenticando...")
                resp_auth = requests.post(SESSION_URL, json={"identifier": usuario, "password": senha})
                resp_auth.raise_for_status()
                token   = resp_auth.json()["accessJwt"]
                HEADERS = {"Authorization": f"Bearer {token}"}
                time.sleep(1)
                continue
            if status == 429:
                print("⏳ Rate-limit atingido. Aguardando 30 segundos...")
                time.sleep(30)
                continue

            print(f"❌ Erro HTTP inesperado: {e}")
            break

        except requests.exceptions.RequestException as e:
            print(f"❌ Falha de rede: {e}")
            time.sleep(5)
            continue
        posts_pagina = dados.get("posts", [])

        if not posts_pagina:
            print("⚠️ Fim de dados na janela atual. Alternando ordenação...")
            ordenacao_atual = "top" if ordenacao_atual == "latest" else "latest"
            cursor = None
            time.sleep(1)
            continue

        for post in posts_pagina:
            try:
                post_id    = post.get("uri", "").split("/")[-1]
                data_post  = post.get("record", {}).get("createdAt", "")
                handle     = post.get("author", {}).get("handle", "")
                texto      = post.get("record", {}).get("text", "")
                like_count = post.get("likeCount", 0)

                if not texto:
                    continue

                texto_linha = texto.replace("\n", " ").replace("\r", " ")
                writer.writerow([post_id, data_post, handle, texto_linha, like_count])
                total_coletados += 1

                if total_coletados >= posts_desejados:
                    break

            except Exception:
                continue

        print(f"-> Progresso: {total_coletados}/{posts_desejados} posts armazenados...")

        if total_coletados >= posts_desejados:
            break

        cursor = dados.get("cursor")
        if not cursor:
            ordenacao_atual = "top" if ordenacao_atual == "latest" else "latest"

        time.sleep(1)  
print(f"💾 Coleta concluída com sucesso! Arquivo '{nome_arquivo}' gerado com {total_coletados} linhas.")