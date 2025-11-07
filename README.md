# PoC: Agente de Chat RAG com Ollama e LlamaIndex

Protótipo (Proof of Concept) de um agente de chat local que usa RAG (Retrieval-Augmented Generation). Permite perguntas em linguagem natural com respostas baseadas apenas em documentos locais (PDF, TXT, etc.).

---

## Visão geral

- LlamaIndex: orquestra o RAG (indexação, busca e composição de prompt).
- Ollama: executa os modelos localmente (LLM principal + embeddings).
- Flask: backend simples que atende o frontend (chatfullscreen.html).
- Dados: pasta `dados_intelbras` com arquivos de conhecimento (manuais, PDFs, TXT).

---

## Como funciona (fluxo)

1. Usuário envia pergunta pelo frontend.
2. Backend (`app.py`) recebe a pergunta.
3. LlamaIndex:
   - Gera embeddings com `nomic-embed-text`.
   - Recupera trechos relevantes da pasta `dados_intelbras`.
   - Monta prompt contendo contexto + pergunta.
4. Ollama:
   - Recebe o prompt e usa o modelo principal (`phi-3`) para gerar resposta.
5. Resposta é enviada ao frontend.

---

## Requisitos

- Python 3.11 (3.12/3.13 podem causar erros de dependência)
- Ollama instalado e rodando (background)
- RAM: >= 16 GB recomendados
- Pasta `dados_intelbras` no mesmo diretório do `app.py` com seus documentos

---

## Preparação (passo a passo)

1. Instalar modelos Ollama (com Ollama rodando):
```powershell
# Modelo LLM principal
ollama pull phi-3:3.8b-mini-128k-instruct-q4_K_M

# Modelo de embeddings
ollama pull nomic-embed-text
```

2. Criar ambiente virtual (Windows / PowerShell):
```powershell
# Navegue até a pasta do projeto
cd C:\Caminho\Para\Seu\Projeto

# Crie venv com Python 3.11
py -3.11 -m venv .venv

# Permitir execução de scripts nesta sessão
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Ativar o ambiente
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependências:
```powershell
# Limpa cache pip (opcional/recomendado)
python -m pip cache purge

# Instala todas as bibliotecas necessárias
python -m pip install --no-cache-dir --upgrade llama-index llama-index-llms-ollama llama-index-embeddings-ollama flask flask-cors pypdf
```

---

## Executando o projeto

1. Verifique se o Ollama está rodando.
2. No terminal (com .venv ativado):
```powershell
python app.py
```
3. Aguarde a mensagem: `INFO:root:Query Engine está pronto. Servidor pronto para receber perguntas.`
4. Abra `chatfullscreen.html` no navegador (duplo clique) e teste o chat.
5. Para parar o servidor: Ctrl + C.

---

## Troubleshooting (problemas comuns)

- ERRO: model requires more system memory...
  - Causa: Ollama tentando carregar modelo antigo ou "fantasma".
  - Solução:
    1. Pare o servidor (Ctrl + C).
    2. Reinicie o app Ollama (ícone da bandeja → Quit) ou finalize `ollama.exe` no Gerenciador de Tarefas.
    3. Reinicie Ollama e rode `python app.py`.

- ERRO: model ... not found (404)
  - Causa: Nome do modelo em `app.py` (linha de Settings.llm) difere do nome em Ollama.
  - Solução:
    1. Rode `ollama list`.
    2. Copie o nome exato do modelo e cole em `app.py` (Settings.llm = Ollama(model="...")).

- ERRO: ModuleNotFoundError / ImportError
  - Causa: Ambiente virtual não ativado.
  - Solução:
    1. Pare o script (Ctrl + C).
    2. Ative o venv: `.\.venv\Scripts\Activate.ps1`.
    3. Rode novamente `python app.py`.

---

## Observações

- Use Python 3.11 precisamente para evitar conflitos de dependência.
- Garanta que a pasta `dados_intelbras` contenha os arquivos que quer indexar.
- Ajuste nomes de modelos em `app.py` conforme aparecem em `ollama list`.

---

Se quiser, eu posso:
- Gerar um arquivo LICENSE.
- Adicionar um badge de status ou exemplo de cURL para a API.
- Otimizar instruções de instalação para Linux/macOS.
