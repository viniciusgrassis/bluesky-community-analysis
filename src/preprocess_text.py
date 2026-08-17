import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True) 
nltk.download('stopwords', quiet=True)

nome_entrada = "dataset_pokemon_texto_bruto.csv"
nome_saida = "dataset_pokemon_texto_processado.csv"

df = pd.read_csv(nome_entrada)
print(f"📊 Dataset bruto carregado: {df.shape[0]} postagens para pré-processamento.")

stopwords_pt = set(stopwords.words('portuguese'))
stopwords_en = set(stopwords.words('english'))
stopwords_totais = stopwords_pt.union(stopwords_en).union({'pokemon', 'pokémon'})

stemmer_pt = SnowballStemmer('portuguese')
stemmer_en = SnowballStemmer('english')

def executar_pipeline_pln(texto_bruto):
    if not isinstance(texto_bruto, str):
        return ""
        
    texto_limpo = re.sub(r'https?://\s*\S+|www\.\S+', '', texto_bruto)
    texto_limpo = re.sub(r'@\S+', '', texto_limpo)
    texto_limpo = re.sub(r'[^a-zA-ZáàâãéèêíïóôõöúçÑñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇ\s]', '', texto_limpo)
    
    texto_minusculo = texto_limpo.lower()
    
    tokens = word_tokenize(texto_minusculo)
    
    tokens_sem_stopwords = [t for t in tokens if t not in stopwords_totais and len(t) > 2]
    
    tokens_stemmed = []
    for token in tokens_sem_stopwords:
        if token in stopwords_pt:
            tokens_stemmed.append(stemmer_pt.stem(token))
        else:
            tokens_stemmed.append(stemmer_en.stem(token))
            
    return " ".join(tokens_stemmed)

print("🧹 Executando o pipeline de Text Mining em cada publicação...")
df['texto_limpo'] = df['texto_bruto'].apply(executar_pipeline_pln)

df = df[df['texto_limpo'] != ""]
print(f"✨ Processamento concluído. {df.shape[0]} postagens válidas restantes.")

df.to_csv(nome_saida, index=False, encoding="utf-8")
print(f"💾 Arquivo intermediário '{nome_saida}' gravado com sucesso.")