import faiss
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import CrossEncoder

# Load once (IMPORTANT for performance)

DATA_PATH = "data"

loader = DirectoryLoader(
    DATA_PATH,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(docs)

for i, doc in enumerate(split_docs):
    doc.metadata["chunk_id"] = i

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

index = faiss.IndexFlatL2(384)

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vector_store.add_documents(split_docs)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

llm = ChatOllama(model="llama3.2")

prompt = ChatPromptTemplate.from_template("""
You are a factual assistant.

Rules:
- Answer ONLY using the provided context
- If not found, say: Not found in the document

Context:
{context}

Question:
{question}

Answer:
""")

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def ask(query: str):
    initial_docs = retriever.invoke(query)

    pairs = [(query, doc.page_content) for doc in initial_docs]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(scores, initial_docs), key=lambda x: x[0], reverse=True)
    final_docs = [doc for _, doc in ranked[:3]]

    context = "\n\n".join([doc.page_content for doc in final_docs])

    response = llm.invoke(prompt.format(context=context, question=query))

    return {
        "answer": response.content,
        "sources": [
            {
                "file": doc.metadata.get("source"),
                "chunk": doc.metadata.get("chunk_id")
            }
            for doc in final_docs
        ]
    }