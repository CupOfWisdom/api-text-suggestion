import os
import requests
from datetime import datetime
from dotenv import load_dotenv  # Importa o dotenv
from groq import Groq

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa o cliente com a API Key
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# URL da sua API REST
API_URL = "http://127.0.0.1:5000/transcription"  # Substitua pela URL real da sua API

try:
    # Faz a requisição GET
    response = requests.get(API_URL)
    response.raise_for_status()  
    res = response.json()  
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    res = "Erro ao obter os dados da API"

# Converte o JSON para string para ser usado no prompt
trancript = res["transcription"]


prompt = f"Analise de forma curta esse trascript de video: {trancript}"

# Faz a requisição para o modelo
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
)

ai_response = chat_completion.choices[0].message.content

log_entry = f"{datetime.now()}:\n - trascript do video: {trancript}\n - resposta da IA: {ai_response}\n\n\n"

with open("log.txt", "a", encoding="utf-8") as f:
    f.write(log_entry)

# Exibe a resposta
print(ai_response)
