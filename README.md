PoC: Agente de Chat RAG com Ollama e LlamaIndex
Este é um protótipo (Proof of Concept) de um agente de chat local que utiliza a técnica RAG (Retrieval-Augmented Generation). O objetivo é permitir que um usuário faça perguntas em linguagem natural e receba respostas baseadas apenas em um conjunto de documentos locais (PDFs, TXTs, etc.).

Este projeto usa LlamaIndex para orquestrar o RAG, Ollama para rodar os modelos de IA localmente, e Flask para servir como um backend de API simples.

🚀 Como Funciona
A arquitetura é dividida em quatro componentes principais:

Frontend (chatfullscreen.html): Uma interface de chat simples onde o usuário envia perguntas.

Backend (app.py): Um servidor Flask que "ouve" o frontend. Ele recebe a pergunta do usuário.

RAG (LlamaIndex): O "cérebro" do backend. Quando recebe uma pergunta:

Ele usa o modelo de embedding (nomic-embed-text) para "entender" o significado da pergunta.

Ele busca nos documentos da pasta dados_intelbras pelos trechos mais relevantes.

Ele monta um novo prompt para o LLM, contendo a pergunta do usuário e os trechos de contexto encontrados.

IA Local (Ollama): O "motor" de IA.

Ele serve o modelo de embedding (nomic-embed-text).

Ele recebe o prompt do LlamaIndex e usa o LLM principal (phi-3) para gerar a resposta.

📋 Requisitos
Antes de começar, garanta que você tem os seguintes requisitos:

Python: Python 3.11 (versões 3.12 ou 3.13 irão falhar com erros de dependência).

Ollama: O aplicativo Ollama instalado e rodando em segundo plano.

RAM: Pelo menos 16 GB de RAM (o modelo Phi-3 é leve, mas o processo de RAG consome memória).

Arquivos de Dados: Uma pasta chamada dados_intelbras no mesmo diretório do app.py, contendo seus arquivos de conhecimento (ex: manuais em PDF da Intelbras).

🛠️ Configuração do Ambiente
Siga estes passos exatamente para configurar seu ambiente de desenvolvimento.

1. Instalar Python 3.11
Se você não tem o Python 3.11, baixe o instalador do site oficial do Python (Windows 64-bit).

Importante: Durante a instalação, marque a caixa "Add python.exe to PATH".

2. Baixar os Modelos Ollama
Com o Ollama já instalado e rodando, abra um terminal (PowerShell) e puxe os dois modelos que o script app.py utiliza:

PowerShell

# 1. O LLM Principal (o "Cérebro")
ollama pull phi-3:3.8b-mini-128k-instruct-q4_K_M

# 2. O Modelo de Embedding (o "Catalogador")
ollama pull nomic-embed-text
3. Criar o Ambiente Virtual Python
Este passo é crucial para isolar as dependências.

PowerShell

# 1. Navegue até a pasta do seu projeto (ex: hackaton-poc)
cd C:\Caminho\Para\Seu\Projeto

# 2. Crie um ambiente virtual usando Python 3.11
py -3.11 -m venv .venv

# 3. Permita a execução de scripts no PowerShell (apenas para esta janela)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 4. Ative o ambiente virtual
.\.venv\Scripts\Activate.ps1

# O seu prompt deve mudar para: (.venv) PS C:\...
4. Instalar as Dependências
Com o ambiente (.venv) ativo, instale todas as bibliotecas Python de uma vez. O pip cache purge garante que você não use pacotes quebrados de um cache antigo.

PowerShell

# Limpa o cache do pip (recomendado)
python -m pip cache purge

# Instala todas as bibliotecas necessárias
python -m pip install --no-cache-dir --upgrade llama-index llama-index-llms-ollama llama-index-embeddings-ollama flask flask-cors pypdf
🏃 Como Executar
Após a configuração, siga estes passos para rodar o projeto:

Garanta que o Ollama está rodando em segundo plano (verifique o ícone na bandeja do sistema).

Abra seu terminal (PowerShell) na pasta do projeto.

Ative o ambiente virtual (se ainda não estiver ativo):

PowerShell

.\.venv\Scripts\Activate.ps1
Execute o servidor de backend:

PowerShell

python app.py

O terminal mostrará os logs. Espere pela mensagem: INFO:root:Query Engine está pronto. Servidor pronto para receber perguntas.

Abra o arquivo chatfullscreen.html no seu navegador (clique duplo no arquivo).

Agora você pode fazer perguntas no chat.

Para parar o servidor de backend, volte ao terminal e pressione Ctrl + C.

⚠️ Solução de Problemas (Troubleshooting)
ERRO: model requires more system memory...

Causa: O Ollama está "preso" tentando carregar um modelo antigo ou "fantasma" que exige mais RAM do que você tem.

Solução:

Pare o servidor (Ctrl + C).

Reinicie o aplicativo Ollama (clique com o botão direito no ícone da bandeja do sistema > "Quit").

Se isso não funcionar, abra o Gerenciador de Tarefas do Windows (Ctrl+Shift+Esc), vá para "Detalhes", encontre ollama.exe e clique em "Finalizar tarefa".

Reinicie o Ollama e rode o python app.py novamente.

ERRO: model ... not found (status code: 404)

Causa: O nome do modelo no app.py (linha 36) não é exatamente igual ao nome do modelo na sua lista do Ollama.

Solução:

Rode ollama list no terminal.

Copie o nome exato do modelo (ex: phi-3:3.8b-mini-128k-instruct-q4_K_M).

Cole esse nome no app.py na linha Settings.llm = Ollama(model="...").

ERRO: ModuleNotFoundError ou ImportError

Causa: Você não ativou o ambiente virtual antes de rodar o python app.py.

Solução: Pare o script (Ctrl + C), rode .\.venv\Scripts\Activate.ps1 e tente novamente.