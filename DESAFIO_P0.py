import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Lista de modelos por ordem de prioridade (Principal -> Reserves)
MODELOS = [
    "gemini-2.0-flash", 
    "gemini-1.5-flash-8b", 
    "gemini-1.5-pro-latest",
    "gemini-3.6-flash",
    "gemini-2.5-flash"
]

response = None

for modelo in MODELOS:
    try:
        print(f"🔄 Tentando chamada com o modelo: {modelo}...")
        response = client.models.generate_content(
            model=modelo,
            contents="Explique o que é RAG em uma frase."
        )
        print(f"✅ Sucesso utilizando: {modelo}\n")
        break  # Se funcionou, sai do loop!
    except APIError as e:
        print(f"⚠️ Erro no modelo {modelo}: {e.message}")
        print("🔀 Redirecionando para o modelo de reserva...\n")

if response:
    usage = response.usage_metadata
    print(f"Resposta: {response.text}\n")
    print(f"📊 Consumo: {usage.prompt_token_count} entrada + {usage.candidates_token_count} saída = {usage.total_token_count} tokens")
else:
    print("❌ Todos os modelos da lista falharam.")