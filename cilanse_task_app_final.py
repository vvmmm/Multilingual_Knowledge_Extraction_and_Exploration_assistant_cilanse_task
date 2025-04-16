import os
import json
import streamlit as st
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# -------------- Streamlit Config (MUST BE FIRST)
st.set_page_config(page_title="📚 Knowledge Assistant", layout="wide")
st.title("📚 Multilingual Knowledge Extraction & Exploration Assistant")

# -------------- Config
CHROMA_PATH = "D:\\PROGRAMS\\python\\streamlit\\cilans_env\\chroma_db_cilans"
OCR_TEXT_DIR = "D:\\PROGRAMS\\python\\streamlit\\cilans_env\\cleaned_output_cilanse"
API_KEY_PATH = "API_GEMINI.txt"

# -------------- Load API Key
with open(API_KEY_PATH, "r") as f:
    API_KEY = f.read().strip()

# -------------- Text Structuring from OCR
def structure_text(raw_text):
    lines = raw_text.split("\n")
    md_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.isupper() or len(line) < 40:
            md_lines.append(f"### {line}")
        else:
            md_lines.append(line)
    return "\n".join(md_lines)

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                raw = f.read()
                structured = structure_text(raw)
                documents.append(Document(page_content=structured, metadata={"source": filename}))
    return documents

# -------------- Chunking
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

# -------------- Vector DB & Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

# Embed only if vectorstore is empty
if vectorstore._collection.count() == 0:
    st.info("⏳ Loading and embedding OCR documents...")
    docs = load_documents(OCR_TEXT_DIR)
    chunks = chunk_documents(docs)
    BATCH_SIZE = 166
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        vectorstore.add_documents(batch)
        print(f"✅ Inserted batch {i//BATCH_SIZE + 1}")
    st.success(f"✅ Embedded {len(chunks)} chunks into ChromaDB!")

retriever = vectorstore.as_retriever()

# -------------- LLM Setup
llm = ChatGoogleGenerativeAI(api_key=API_KEY, model="gemini-2.0-pro")

PROMPT_TEMPLATE = """
You're an assistant helping users explore knowledge from a digitized textbook.
Use the most relevant chunks from the content to answer the question.

Context:
{context}

Question:
{question}

Answer clearly in the same language as the question.
"""
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
chain = prompt_template | llm | StrOutputParser()

# -------------- UI: Choose Mode
mode = st.selectbox("Select Mode", ["🔎 Keyword Search", "🤖 Ask a Question (LLM)"])

if mode == "🔎 Keyword Search":
    keyword = st.text_input("Enter keyword to search:")
    if keyword:
        st.write("📖 Relevant content:")
        docs = retriever.get_relevant_documents(keyword)
        for i, doc in enumerate(docs[:5], 1):
            st.markdown(f"**Result {i}:** ({doc.metadata.get('source', '')})\n```text\n{doc.page_content[:500]}\n```")

elif mode == "🤖 Ask a Question (LLM)":
    query = st.text_input("Ask your question:")
    if query:
        st.write("🔍 Retrieving content and generating answer...")
        relevant_docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in relevant_docs[:3]])

        with st.spinner("✍️ Generating answer..."):
            result = chain.invoke({"context": context, "question": query})
            st.markdown("### 📖 Answer")
            st.write(result)

            st.markdown("### 📚 Book-like Sources")

            # Add toggle to filter messy results
            filter_garbage = st.toggle("🧹 Filter low-quality content", value=True)

            for i, doc in enumerate(relevant_docs[:5], 1):
                content = doc.page_content.strip()
                source_name = doc.metadata.get("source", f"Document {i}")

                # Check for garbage: short length or low character quality
                is_garbage = (
                    len(content) < 100 or
                    sum(1 for c in content if c.isalpha()) < 30 or
                    content.count("###") > 15
                )

                if filter_garbage and is_garbage:
                    continue

                # Show the source file or fallback
                st.markdown(f"#### 📄 Source {i}: `{source_name}`")

                for line in content.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("### "):
                        st.markdown(f"**{line[4:]}**")  # Treat as sub-heading
                    else:
                        st.markdown(line)

