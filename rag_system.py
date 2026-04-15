from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = None


def load_pdf(file_path):
    global vector_db

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    docs = splitter.split_documents(pages)

    vector_db = FAISS.from_documents(
        docs,
        embedding_model
    )


def search_docs(query):
    global vector_db

    if vector_db is None:
        return ""

    docs = vector_db.similarity_search(query, k=5)

    return "\n".join([doc.page_content for doc in docs])