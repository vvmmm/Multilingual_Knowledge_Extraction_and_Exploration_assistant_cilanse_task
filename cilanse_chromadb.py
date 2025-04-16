from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os

# ----------------------------
# Load OCR extracted text files
loader = DirectoryLoader(
    "D:/PROGRAMS/python/streamlit/cilans_env/output_cilanse",  # OCR text output folder
    glob="*.txt",
    show_progress=True,
    loader_cls=lambda path: TextLoader(path, encoding="utf-8")
)

docs = loader.load()

# ----------------------------
# Split into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

print("✅ Number of Documents:", len(docs))
print("✅ Number of Chunks:", len(chunks))

# ----------------------------
# Load Google GenAI Embeddings
with open("API_GEMINI.txt", "r") as file:
    key = file.read().strip()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=key
)

# ----------------------------
# Initialize Chroma DB
db = Chroma(
    collection_name="cilans_vector_db",
    embedding_function=embeddings,
    persist_directory="./chroma_db_cilans"
)

# ----------------------------
# Insert documents in batches
batch_size = 100
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    db.add_documents(batch)
    print(f"✅ Inserted batch {i//batch_size + 1}")

print("🎉 All OCR chunks embedded and stored in ChromaDB!")
