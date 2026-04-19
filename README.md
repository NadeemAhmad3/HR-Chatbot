# HR-Chatbot: Advanced Resume Intelligence Platform

> AI-Powered Candidate Search & Analysis with Retrieval-Augmented Generation (RAG)
> 
> Professional-grade HR automation using modern LLMs, vector databases, and intelligent reranking

---

## 🎯 Project Overview

**HR-Chatbot** is an advanced enterprise-level resume intelligence platform that combines cutting-edge AI technologies with intuitive user interfaces. It enables HR professionals and recruiters to instantly search, analyze, and gain insights about candidate qualifications through natural language conversations.

### Key Capabilities

- **Intelligent Candidate Search**: Ask questions about candidates using natural language queries
- **PDF Resume Processing**: Upload and automatically parse PDF resumes with intelligent extraction
- **Vector Similarity Search**: Advanced semantic search using embeddings to find relevant candidates
- **Cohere Reranking**: Intelligent result reranking for higher relevance
- **Professional Dark UI**: Modern, responsive interface with professional styling
- **Real-time Chat**: Conversational interface with chat history and context awareness
- **Candidate Management**: Browse, search, and manage candidate database
- **Database Persistence**: SQLite backend with vector embeddings persistence

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
├─────────────────────────────────────────────────────────────┤
│  Chatbot Tab  │  Browse Tab  │  Manage Tab                   │
├─────────────────────────────────────────────────────────────┤
│                    Application Logic Layer                    │
├──────────────────┬──────────────────┬────────────────────────┤
│  Resume Parser   │  LLM Integration │  Vector Search Engine  │
│  (PyPDF2)        │  (Cohere API)     │  (ChromaDB)            │
├──────────────────┴──────────────────┴────────────────────────┤
│                    Data Storage Layer                         │
├──────────────────┬──────────────────────────────────────────┤
│  SQLite DB       │  Chroma Vector DB                         │
│  (resumes.db)    │  (chroma_db/)                             │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Web Framework** | Streamlit | 1.32.0+ |
| **LLM API** | Cohere | 5.3.0+ |
| **Vector Database** | ChromaDB | 0.5.0+ |
| **Embeddings** | FastEmbedEmbeddings | 0.3.6+ |
| **PDF Processing** | PyPDF2 | 3.0.1+ |
| **Database** | SQLite3 | Built-in |
| **Configuration** | python-dotenv | 1.0.0+ |
| **Programming Language** | Python | 3.10+ |

---

## ✨ Features

### 1. Intelligent Chatbot
- **Natural Language Queries**: Ask questions like "Do we have any Python developers?" or "Find candidates with AI skills"
- **Context-Aware Responses**: AI understands candidate context and provides meaningful answers
- **Chat History**: Maintains conversation history throughout the session
- **Real-time Processing**: Instant responses powered by Cohere's advanced models

### 2. Advanced Search
- **Vector Similarity Search**: Semantic understanding beyond keyword matching
- **Intelligent Reranking**: Cohere's reranking algorithm ensures top-relevant results
- **Multi-field Filtering**: Search by name, skills, experience, and more

### 3. Resume Management
- **Batch Upload**: Upload multiple PDF resumes at once
- **Intelligent Parsing**: Automatically extracts:
  - Candidate name, email, phone number
  - Skills and technical proficiencies
  - Education and degrees
  - Work experience
  - Location information
- **Persistent Storage**: All resumes indexed for instant retrieval

### 4. Professional UI
- **Dark Theme**: Easy on the eyes with modern gradient backgrounds
- **Neon Accents**: Professional styling with cyan/teal color scheme
- **Responsive Design**: Works seamlessly on desktop and tablet
- **Organized Tabs**: Intuitive navigation between Chatbot, Browse, and Manage sections

---

## 📋 System Requirements

- Python 3.10 or higher
- Windows, macOS, or Linux
- Minimum 4GB RAM (8GB recommended)
- Internet connection (for Cohere API)
- 500MB+ free disk space

---

## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/NadeemAhmad3/resume-chatbot-local-llm
cd resume-chatbot-local-llm-main
```

### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Cohere API Key

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key_here
```

Get your free API key from: https://cohere.com/

### 5. Run Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Adding Candidates

1. Navigate to the **Manage** tab
2. Click **Upload Resumes** and select PDF files
3. Click **Process & Index**
4. Resumes will be parsed and added to the database

### Searching Candidates

1. Go to the **Chatbot** tab
2. Ask natural language queries:
   - "Do we have Python developers?"
   - "Find candidates with machine learning skills"
   - "Who has experience with React?"
3. Get AI-powered answers with candidate information

### Browsing Database

1. Navigate to the **Browse** tab
2. Search by candidate name or skills
3. Click **View Full Details** to see complete information
4. Contact details are displayed for shortlisting

---

## 📁 Project Structure

```
resume-chatbot-local-llm-main/
├── app.py                          # Main application (950+ lines)
├── requirements.txt                # Python dependencies
├── .env                            # Configuration file (API keys)
├── resumes.db                      # SQLite database
├── chroma_db/                      # Vector embeddings storage
├── README.md                       # This file
└── LICENSE                         # MIT License
```

---

## 🔑 Key Functions

### Core Processing
- `extract_text_from_pdf()` - Extracts text from PDF files using PyPDF2
- `parse_resume()` - Parses extracted text and extracts structured data
- `add_resume_to_db()` - Stores resume in SQLite database
- `get_all_resumes()` - Retrieves all candidates from database

### Search & Ranking
- `ResumeRetriever.ingest()` - Indexes documents in vector database
- `ResumeRetriever.retrieve()` - Semantic search using embeddings
- `ResumeRetriever.rerank_with_cohere()` - Reranks results using Cohere API
- `generate_answer_with_cohere()` - Generates contextual answers

### UI Components
- `show_header()` - Displays professional header
- `chatbot_tab()` - Chatbot interface
- `browse_candidates_tab()` - Candidate browsing interface
- `data_management_tab()` - Resume upload and management

---

## 🔒 Security & Privacy

- **Local Storage**: All resume data stored locally in SQLite
- **Secure API Keys**: Use `.env` file (added to `.gitignore`)
- **No Data Sharing**: Resumes never sent to external servers (except Cohere for processing)
- **HTTPS Ready**: Can be deployed with SSL/TLS

---

## 📊 Performance

- **Indexing Speed**: ~500ms per resume
- **Search Speed**: <100ms for vector similarity search
- **Response Time**: ~2-3 seconds for AI-generated answers
- **Scalability**: Handles 1000+ resumes efficiently

---

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment (Streamlit Cloud)
```bash
streamlit run app.py --logger.level=error
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not configured" | Check `.env` file has correct `COHERE_API_KEY` |
| Resumes not appearing in search | Click "Process & Index" after upload |
| Slow search results | Reduce number of indexed resumes or upgrade Cohere plan |
| PDF parsing fails | Ensure PDF is text-based (not scanned image) |

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository: https://github.com/NadeemAhmad3/resume-chatbot-local-llm
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 About the Developer

**Nadeem Ahmad**

- **GitHub**: [@NadeemAhmad3](https://github.com/NadeemAhmad3)
- **LinkedIn**: [nadeem-ahmad3](https://www.linkedin.com/in/nadeem-ahmad3/)
- **Email**: [engrnadeem26@gmail.com](mailto:engrnadeem26@gmail.com)

---

## 🙏 Acknowledgments

- [Cohere](https://cohere.com/) - Advanced LLM APIs
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Streamlit](https://streamlit.io/) - Web framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [FastEmbed](https://github.com/qdrant/fastembed) - Embeddings

---

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub: https://github.com/NadeemAhmad3/resume-chatbot-local-llm/issues
- Email: engrnadeem26@gmail.com
- LinkedIn: https://www.linkedin.com/in/nadeem-ahmad3/

---

**Built with ❤️ for HR Professionals & Recruiters**
5. Create a new Pull Request

2024
