from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore import InMemoryDocstore
import os

# Create embeddings (using a free local model)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vectorstore(chunks, persist_path="faiss_index"):
    texts = [chunk['text'] for chunk in chunks]
    metadatas = [chunk.get('metadata', {}) for chunk in chunks]
    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    vectorstore.save_local(persist_path)
    return vectorstore

def load_vectorstore(persist_path="faiss_index"):
    if not os.path.exists(persist_path):
        raise ValueError("Vectorstore not found, please run training first!")
    vectorstore = FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

def search_vectorstore(query, k=3):
    vectorstore = load_vectorstore()
    docs_and_scores = vectorstore.similarity_search_with_score(query, k=k)
    # Combine texts of top k chunks
    combined_text = "\n\n".join([doc.page_content for doc, score in docs_and_scores])
    return combined_text
