import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

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
        
        # Lista com prioridade de modelos para a interface
        MODELOS = ["gemini-3.6-flash", "gemini-2.5-flash"]
        response = None
        
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            
            # Loop de resiliência (Fallback) dentro do app
            for modelo in MODELOS:
                try:
                    print(f"🔄 [BACKEND LOG] Tentando modelo: {modelo}")
                    response = client.models.generate_content(
                        model=modelo,
                        contents=prompt
                    )
                    print(f"✅ [BACKEND LOG] Sucesso no modelo: {modelo}")
                    break 
                except APIError as e:
                    print(f"⚠️ [BACKEND LOG] Erro no modelo {modelo}: {e.message}")
            
            # Exibição do resultado se algum modelo respondeu
            if response:
                resposta_texto = response.text
                message_placeholder.markdown(resposta_texto)
                st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                
                # Métricas de consumo apenas no terminal de dev
                usage = response.usage_metadata
                print(f"📊 [BACKEND METRICS] Consumo real: {usage.prompt_token_count} in / {usage.candidates_token_count} out.")
            else:
                message_placeholder.error("Não foi possível obter resposta de nenhum modelo disponível no momento.")

        except Exception as e:
            message_placeholder.error("Ocorreu um erro ao processar sua solicitação.")
            print(f"❌ [BACKEND LOG CRÍTICO] {e}")