# 📚 Multilingual Knowledge Extraction & Exploration Assistant

A Streamlit-based intelligent assistant that enables **search and question-answering** over digitized **handwritten multilingual textbooks** using OCR, semantic embeddings, and generative AI.

---

## 🔧 Project Overview

This application is designed to help users **interactively explore handwritten textbooks** that have been digitized using OCR. Users can either search using keywords or ask natural language questions, and the system returns context-aware results in a book-like format.

---

## 💡 Key Features

- 📖 Extract structured content from raw OCR text files
- 🌍 Multilingual support for both keyword and semantic search
- 🔍 Fast semantic retrieval using ChromaDB & Gemini embeddings
- 🤖 Natural language question answering using Gemini Pro
- 📐 Structured formatting of results, preserving logical document flow

---

## 🛠️ Models, Tools & Techniques

| Component              | Tool / Model                          | Purpose                                       |
|------------------------|----------------------------------------|-----------------------------------------------|
| UI                     | Streamlit                              | User-friendly front-end                       |
| OCR Input              | Parsed `.txt` files                    | Handwritten content digitized externally      |
| Vector Store           | [ChromaDB](https://www.trychroma.com/) | Fast semantic search                          |
| Embeddings             | Google Gemini Embeddings (`embedding-001`) | Multilingual chunk encoding              |
| LLM for QA             | Gemini Pro (`gemini-2.0-pro`)         | Question answering based on context chunks    |
| Prompt Design          | LangChain PromptTemplate               | Prompt engineering for accurate QA            |
| Chunking               | RecursiveCharacterTextSplitter         | Adaptive chunk creation from structured text  |

---

## ✅ What Worked Well

- **Embedding + ChromaDB Integration**: Enabled fast and accurate semantic retrieval.
- **Gemini Pro QA**: Gave coherent, contextual answers in both English and Hindi.
- **Structured Output Display**: Enhanced readability by rendering retrieved chunks like textbook sections.
- **Multilingual Handling**: Gemini's multilingual embeddings worked seamlessly with Hindi, Sanskrit, and English.

---

## ❌ Challenges & What Didn’t Work

- **OCR Garbling**: Some scanned text chunks had noise or formatting errors, leading to irrelevant or unreadable results.
- **Whisper Redundancy**: Initially imported Whisper for ASR, but since input was OCR text, it was removed to reduce dependencies.
- **Chunk Quality**: OCR text sometimes split poorly due to inconsistent line breaks or formatting in scanned material.

---

## 🌐 Handling Handwritten & Multilingual Content

- Handwritten content was assumed to be pre-parsed using an external OCR pipeline (not in this repo).
- Structured the OCR text by detecting headings and segmenting content logically.
- Used **Google Gemini embeddings**, which are inherently multilingual, allowing accurate cross-lingual semantic matching.

---

## ⚖️ Design Decisions & Trade-offs

- Chose **Gemini over OpenAI** for seamless multilingual support and low-latency embeddings.
- Avoided heavy OCR processing within the app to keep runtime lean and modular.
- Limited results to top 3 chunks for QA to balance between relevance and generation performance.
- Used only text-based OCR for now; layout-aware parsing (e.g., table handling) is not yet integrated.

---

## 🔮 Future Improvements

- 🖼️ Add **layout-aware OCR (e.g., Donut or LayoutLMv3)** for better structure retention.
- 🌐 Integrate **speech or video-based textbook content** via Whisper or AV parsing.
- 📝 Enable **editing or feedback on incorrect OCR sections** directly from UI.
- 📊 Add analytics or usage tracking to see which queries return poor results.
- 🌍 Expand to support **other scripts** like Urdu, Tamil, or Bengali.

---

## 🚀 Getting Started

```bash
# Clone repo and install dependencies
git clone https://github.com/vvmmm/Multilingual_Knowledge_Extraction_and_Exploration_assistant_cilanse_task
cd knowledge-assistant
pip install -r requirements.txt

# Run the Streamlit app
streamlit run cilanse_task_app_final.py
