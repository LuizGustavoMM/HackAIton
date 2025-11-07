import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS 

# --- IMPORTAÇÕES CORRIGIDAS ---
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama 
from llama_index.embeddings.ollama import OllamaEmbedding
# --- FIM DAS IMPORTAÇÕES ---

# --- Configuração de Logging (Bom para debug) ---
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# --- 1. Inicialização do Aplicativo Flask ---
app = Flask(__name__)
CORS(app) 

# --- 2. Configuração Global do LlamaIndex (RAG) ---
query_engine = None

def initialize_rag():
    global query_engine
    try:
        # --- Configurar os Modelos do Ollama ---
        
        # O "Cérebro" (LLM) - Usando phi3:3.8b-mini-128k-instruct-q4_K_M
        Settings.llm = Ollama(model="phi3:3.8b-mini-128k-instruct-q4_K_M", request_timeout=120.0)

        # O "Catalogador" (Embedding)
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

        # --- Carregar e Indexar os Dados ---
        logging.info("Carregando documentos da pasta 'dados_intelbras'...")
        documents = SimpleDirectoryReader("./dados_intelbras").load_data()
        
        if not documents:
            logging.error("Nenhum documento encontrado em './dados_intelbras'.")
            logging.error("Por favor, adicione PDFs ou arquivos .txt e reinicie o servidor.")
            sys.exit(1)

        logging.info(f"Total de {len(documents)} documentos carregados.")
        
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        Settings.node_parser = splitter

        logging.info("Criando o índice (isso pode demorar)...")
        index = VectorStoreIndex.from_documents(documents)
        logging.info("Índice criado com sucesso!")

        # --- Criar o "Motor de Pergunta" ---
        query_engine = index.as_query_engine(similarity_top_k=3, streaming=False)
        logging.info("Query Engine está pronto. Servidor pronto para receber perguntas.")

    except Exception as e:
        logging.error(f"Erro fatal durante a inicialização do RAG: {e}")
        sys.exit(1)

# --- 3. Criação do Endpoint da API ---
@app.route('/api/ask', methods=['POST'])
def ask_question():
    if not query_engine:
        return jsonify({"error": "O Query Engine não foi inicializado."}), 500

    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({"error": "Nenhuma pergunta ('question') foi fornecida."}), 400

    logging.info(f"Recebida nova pergunta: {question}")
    
    try:
        response = query_engine.query(question)
        answer = str(response)
        
        logging.info(f"Resposta gerada: {answer}")
        
        return jsonify({"answer": answer})

    except Exception as e:
        logging.error(f"Erro ao processar a pergunta: {e}")
        return jsonify({"error": f"Erro no servidor ao processar a pergunta: {e}"}), 500

# --- 4. Iniciar o Servidor ---
if __name__ == '__main__':
    initialize_rag()
    app.run(host='0.0.0.0', port=5000, debug=True)