# 🤖 Residência Tecnológica em IA - Módulo P0

Aplicação interativa de chat e backend resiliente construído com Python, a nova SDK oficial do Google Gemini e Streamlit.

## 🚀 Funcionalidades (P0)
* **Backend Resiliente:** Sistema de *fallback* automático de modelos (`gemini-3.6-flash`, `gemini-2.5-flash`) em caso de indisponibilidade da API.
* **Telemetria e Controle de Tokens:** Monitorização em tempo real do consumo de tokens de entrada e saída no terminal do desenvolvedor.
* **Segurança e Proteção de Dados:** Isolamento de credenciais e chaves de API via variáveis de ambiente (`.env`) e exclusão no `.gitignore`.
* **Interface do Utilizador:** Chatbot interativo em Streamlit com mensagens amigáveis de tratamento de erros para o cliente final.

## 🛠️ Como Executar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/fefeluis91-crypto/MINI-PROJETO-4.git](https://github.com/fefeluis91-crypto/MINI-PROJETO-4.git)
   cd MINI-PROJETO-4