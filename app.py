import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

PRECO_ENTRADA_PER_1M = 0.075
PRECO_SAIDA_PER_1M = 0.30

st.title("🤖 Meu Primeiro Chatbot com IA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Apenas modelos válidos e operacionais
        MODELOS = ["gemini-3.6-flash", 
                   "gemini-1.5-flash",
                   "gemini-2.5-flash",        
                    "gemini-1.5-flash-latest", 
                    "gemini-1.5-pro-latest",
                    "gemini-2.0-flash",       
                    "gemini-1.5-flash-8b",    
                    "gemini-2.0-flash-lite"
                ]
        response = None
        tempo_inicio_total = time.time()
        
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            
            for modelo in MODELOS:
                print(f"\n🎯 [BACKEND LOG] A tentar modelo: {modelo}")
                
                
                for tentativa in range(1, 5):
                    tempo_inicio_tentativa = time.time()
                    print(f"🔄 [BACKEND LOG] Tentativa {tentativa}/5 em {modelo}...")
                    
                    try:
                        # Chamada simples e direta
                        response = client.models.generate_content(
                            model=modelo,
                            contents=prompt,
                            config={"system_instruction": "Você é um assistente prestativo. Responda sempre em português do Brasil."}
                        )
                        
                        tempo_execucao = time.time() - tempo_inicio_tentativa
                        print(f"✅ [BACKEND LOG] Sucesso em {modelo} ({tempo_execucao:.2f}s)")
                        break
                        
                    except APIError as e:
                        tempo_falha = time.time() - tempo_inicio_tentativa
                        print(f"⚠️ [BACKEND LOG] Erro no modelo {modelo} em {tempo_falha:.2f}s: {e.message}")
                        
                        # Se for alta procura, aguarda apenas 1s
                        if "high demand" in str(e).lower() or "503" in str(e).lower():
                            time.sleep(1)
                        else:
                            break # Erro estrutural: passa logo ao modelo seguinte
                
                if response:
                    break # Resposta obtida, interrompe a procura na lista de modelos
            
            tempo_total = time.time() - tempo_inicio_total
            
            if response:
                resposta_texto = response.text
                message_placeholder.markdown(resposta_texto)
                st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                
                # Extração e Cálculo Financeiro dos Tokens (Completão)
                usage = response.usage_metadata
                tokens_in = usage.prompt_token_count
                tokens_out = usage.candidates_token_count
                tokens_total = usage.total_token_count
                
                custo_in = (tokens_in / 1_000_000) * PRECO_ENTRADA_PER_1M
                custo_out = (tokens_out / 1_000_000) * PRECO_SAIDA_PER_1M
                custo_total_usd = custo_in + custo_out
                
                print(f"\n📊 --- RELATÓRIO DE TELEMETRIA E CUSTO DETALHADO ---")
                print(f"⏱️ Tempo de processamento da API: {tempo_total:.2f} segundos")
                print(f"📥 Tokens de Entrada (Seu prompt + System Instruction): {tokens_in}")
                print(f"📤 Tokens de Saída (Resposta do Gemini): {tokens_out}")
                print(f"👻 Tokens Fantasmas (Filtros do Google e AFC): {tokens_total - (tokens_in + tokens_out)}")
                print(f"🧮 Tokens Totais Consumidos na API: {tokens_total}")
                print(f"💵 Custo Estimado da Requisição: ${custo_total_usd:.7f} USD")
                print(f"------------------------------------------------------\n")
            else:
                message_placeholder.error("Serviço indisponível no momento. Tente novamente em instantes.")
                print(f"❌ [BACKEND LOG] Falha geral após {tempo_total:.2f}s.")

        except Exception as e:
            message_placeholder.error("Ocorreu um erro interno.")
            print(f"❌ [BACKEND LOG CRÍTICO] {e}")