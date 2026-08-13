# AI Portfolio Assistant — RAG Chatbot

An AI-powered chatbot built for my personal portfolio that allows visitors to ask questions about my **projects, skills, certifications, internships, education, and experience**.

The chatbot uses a **Retrieval-Augmented Generation (RAG)** architecture so that responses are generated from information stored in my portfolio knowledge base rather than relying only on the LLM's general knowledge.

**Live Demo:**  
https://jeevanakasturi-portfolio.netlify.app

---

# Project Overview

I wanted to build a chatbot that could understand my portfolio and answer questions about it in a natural way.

Instead of sending the entire portfolio content to an LLM for every question, I built a RAG pipeline that:

1. Collects content from my portfolio website
2. Cleans and processes the content
3. Splits the content into smaller chunks
4. Converts the chunks into vector embeddings
5. Stores the embeddings in a vector database
6. Converts the user's question into an embedding
7. Retrieves the most relevant portfolio information
8. Sends the retrieved information to an LLM
9. Generates a concise, context-grounded answer

---

# 🏗️ System Architecture

```text
                    PORTFOLIO WEBSITE
                           │
                           ▼
                    Website Crawler
                           │
                           ▼
                     HTML Parser
                           │
                           ▼
                      Chunking
                           │
                           ▼
                SentenceTransformer
                 (all-MiniLM-L6-v2)
                           │
                           ▼
                       Embeddings
                           │
                           ▼
                       ChromaDB
                  Vector Database
                           │
                           │
                    USER QUESTION
                           │
                           ▼
                SentenceTransformer
                           │
                           ▼
                   Query Embedding
                           │
                           ▼
                 Semantic Retrieval
                           │
                           ▼
              Relevant Portfolio Chunks
                           │
                           ▼
                      Groq API
                           │
                           ▼
                         LLM
                           │
                           ▼
                  Generated Answer
                           │
                           ▼
                    Gradio API
                           │
                           ▼
                 Portfolio Frontend
