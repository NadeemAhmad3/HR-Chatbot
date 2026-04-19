"""
HR-Chatbot: Advanced Resume Intelligence Platform
Professional Grade AI-Powered Candidate Analysis & Search
Dark Theme with Neon Accents | Powered by Cohere & ChromaDB
"""

import os
from dotenv import load_dotenv
import json
import tempfile
import sqlite3
import re
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import streamlit as st
from streamlit_chat import message
import pandas as pd
import cohere
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import PyPDF2

# Load environment variables from .env file
load_dotenv()

# =====================================================================
# CONFIGURATION
# =====================================================================

DB_PATH = "resumes.db"
VECTOR_DB_PATH = "./chroma_db"
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

# =====================================================================
# PAGE CONFIGURATION
# =====================================================================

st.set_page_config(
    page_title="HR-Chatbot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# PROFESSIONAL CSS STYLING - DARK THEME WITH NEON ACCENTS
# =====================================================================

st.markdown("""
<style>
    /* ===== GLOBAL STYLES ===== */
    * {
        font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
    }
    
    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    
    /* Global dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #e2e8f0;
    }
    
    /* Header background */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Block container - proper spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 1400px !important;
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    
    p, span, div, label {
        color: #e2e8f0 !important;
    }
    
    /* Main header with neon glow - MAKE IT VISIBLE */
    .main-header {
        font-size: 3.2rem;
        font-weight: 900;
        text-align: center;
        color: #00f5ff;
        margin: 2rem 0 1rem 0;
        letter-spacing: 3px;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.8), 
                     0 0 60px rgba(123, 47, 247, 0.6);
        filter: drop-shadow(0 0 20px rgba(0, 245, 255, 0.6));
        display: block;
        visibility: visible;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    /* ===== CARDS & CONTAINERS ===== */
    .stContainer {
        background: rgba(13, 17, 23, 0.8);
        border: 1px solid rgba(48, 54, 61, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Resume card */
    .resume-card {
        background: linear-gradient(135deg, rgba(30, 42, 58, 0.8), rgba(45, 55, 72, 0.8));
        border: 1px solid #30363d;
        border-left: 4px solid #00f5ff;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .resume-card:hover {
        transform: translateX(6px) translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.25);
        border-color: #00f5ff;
    }
    
    /* Info container */
    .info-box {
        background: linear-gradient(135deg, rgba(30, 42, 58, 0.9), rgba(45, 55, 72, 0.9));
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.08);
    }
    
    /* ===== CHAT COMPONENTS ===== */
    .chat-container {
        background: linear-gradient(180deg, rgba(13, 17, 23, 0.95), rgba(22, 27, 34, 0.95));
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        min-height: 500px;
        max-height: 650px;
        overflow-y: auto;
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.12);
        backdrop-filter: blur(5px);
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(22, 27, 34, 0.8);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00f5ff, #7b2ff7);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00f5ff, #00d4ff);
    }
    
    /* User message */
    .user-message {
        background: linear-gradient(135deg, #7b2ff7, #f72585);
        color: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        border-bottom-right-radius: 4px;
        margin-left: auto;
        margin-right: 0;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(123, 47, 247, 0.4);
        animation: slideInRight 0.3s ease;
    }
    
    /* Bot message */
    .bot-message {
        background: linear-gradient(135deg, rgba(30, 42, 58, 0.95), rgba(45, 55, 72, 0.95));
        color: #e2e8f0;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        border-bottom-left-radius: 4px;
        border: 1px solid #30363d;
        margin-left: 0;
        margin-right: auto;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.15);
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* ===== INPUT COMPONENTS ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00f5ff !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.4) !important;
    }
    
    .stTextInput > label,
    .stTextArea > label {
        color: #8892b0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(22, 27, 34, 0.6);
        border: 2px dashed #30363d;
        border-radius: 12px;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #00f5ff, #7b2ff7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.35) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(0, 245, 255, 0.55) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid #30363d;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(22, 27, 34, 0.7);
        border: 1px solid #30363d;
        border-radius: 10px;
        color: #8892b0;
        padding: 1rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f5ff, #7b2ff7) !important;
        color: white !important;
        border-color: #00f5ff !important;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3) !important;
    }
    
    /* ===== SELECT & DROPDOWN ===== */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    
    .stSelectbox label,
    .stMultiSelect label {
        color: #8892b0 !important;
        font-weight: 600 !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background-color: rgba(22, 27, 34, 0.8);
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(30, 42, 58, 0.9);
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(13, 17, 23, 0.95), rgba(22, 27, 34, 0.95));
        border-right: 1px solid #30363d;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00f5ff !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #8892b0 !important;
    }
    
    /* ===== METRICS ===== */
    .metric-box {
        background: linear-gradient(135deg, #00f5ff, #7b2ff7);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.25);
        color: white;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 600;
    }
    
    /* ===== SOURCE BADGES ===== */
    .source-badge {
        background: linear-gradient(135deg, rgba(30, 42, 58, 0.9), rgba(45, 55, 72, 0.9));
        border-left: 4px solid #00f5ff;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 245, 255, 0.12);
        transition: all 0.3s ease;
    }
    
    .source-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 245, 255, 0.25);
        border-color: #00f5ff;
    }
    
    /* ===== STATUS & FEEDBACK ===== */
    .stWarning, .stInfo, .stSuccess, .stError {
        background-color: rgba(13, 17, 23, 0.9) !important;
        border-radius: 12px !important;
        border: 1px solid #30363d !important;
    }
    
    .stSuccess {
        border-color: #2ecc71 !important;
    }
    
    .stWarning {
        border-color: #f39c12 !important;
    }
    
    .stError {
        border-color: #e74c3c !important;
    }
    
    .stInfo {
        border-color: #00f5ff !important;
    }
    
    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-color: #00f5ff transparent transparent transparent !important;
    }
    
    /* ===== MISC ===== */
    hr {
        border-color: #30363d !important;
        margin: 2rem 0 !important;
    }
    
    .element-container:empty {
        display: none !important;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #8892b0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# DATABASE FUNCTIONS
# =====================================================================

def init_database():
    """Initialize SQLite database with proper schema"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Create resumes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            resume_id TEXT PRIMARY KEY,
            candidate_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            location TEXT,
            raw_text TEXT NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create search history table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()

def add_resume_to_db(resume_id: str, candidate_name: str, raw_text: str, metadata: Dict):
    """Store resume in database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO resumes 
        (resume_id, candidate_name, email, phone, location, raw_text, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            resume_id,
            candidate_name,
            metadata.get('email', ''),
            metadata.get('phone', ''),
            metadata.get('location', ''),
            raw_text,
            json.dumps(metadata)
        ))
        conn.commit()

def get_all_resumes():
    """Retrieve all resumes from database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resumes ORDER BY created_at DESC")
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

# =====================================================================
# RESUME PARSER
# =====================================================================

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file"""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""
    return text

def parse_resume(resume_text: str) -> Dict:
    """Extract structured data from resume text"""
    metadata = {
        'skills': [],
        'email': '',
        'phone': '',
        'location': '',
        'experience_years': 0,
        'education': []
    }
    
    # Extract email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text)
    if email_match:
        metadata['email'] = email_match.group(0)
    
    # Extract phone
    phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', resume_text)
    if phone_match:
        metadata['phone'] = phone_match.group(0)
    
    # Extract skills
    skills_keywords = ['Python', 'JavaScript', 'Java', 'SQL', 'AWS', 'Azure', 'Docker',
                       'Kubernetes', 'React', 'Angular', 'Node.js', 'Django', 'FastAPI',
                       'PostgreSQL', 'MongoDB', 'Git', 'CI/CD', 'Agile', 'Scrum',
                       'Machine Learning', 'TensorFlow', 'PyTorch', 'Data Analysis']
    for skill in skills_keywords:
        if re.search(r'\b' + skill + r'\b', resume_text, re.IGNORECASE):
            metadata['skills'].append(skill)
    
    # Extract education
    education_keywords = ['B.S.', 'M.S.', 'Ph.D.', 'Bachelor', 'Master', 'MBA', 'diploma']
    for edu in education_keywords:
        if re.search(r'\b' + edu + r'\b', resume_text, re.IGNORECASE):
            metadata['education'].append(edu)
    
    # Extract experience years
    exp_match = re.search(r'(\d+)\+?\s*years?(?:\s+of)?\s+(?:experience|exp)', resume_text, re.IGNORECASE)
    if exp_match:
        metadata['experience_years'] = int(exp_match.group(1))
    
    return metadata

# =====================================================================
# RETRIEVER CLASS
# =====================================================================

class ResumeRetriever:
    """Advanced retriever with Cohere reranking"""
    
    def __init__(self):
        self.embeddings = FastEmbedEmbeddings()
        self.vector_store = None
        self.documents_map = {}
        self.cohere_client = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None
        
        # Load existing resumes from database on startup
        self._load_existing_resumes()
    
    def _load_existing_resumes(self):
        """Load all existing resumes from database into vector store"""
        try:
            resumes = get_all_resumes()
            if resumes:
                documents = []
                for resume in resumes:
                    documents.append({
                        'content': resume.get('raw_text', ''),
                        'source': resume.get('resume_id', ''),
                        'candidate_name': resume.get('candidate_name', '')
                    })
                if documents:
                    self.ingest(documents)
        except Exception as e:
            print(f"Error loading existing resumes: {str(e)}")
    
    def ingest(self, documents: List[Dict]):
        """Ingest documents into vector store"""
        if not documents:
            return
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        
        langchain_docs = []
        
        for doc in documents:
            chunks = text_splitter.split_text(doc['content'])
            
            for idx, chunk in enumerate(chunks):
                chunk_id = f"{doc['source']}_chunk_{idx}"
                langchain_docs.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            'chunk_id': chunk_id,
                            'source': doc['source'],
                            'candidate': doc.get('candidate_name', '')
                        }
                    )
                )
                self.documents_map[chunk_id] = chunk
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=langchain_docs,
            embedding=self.embeddings,
            persist_directory=VECTOR_DB_PATH
        )
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve documents using vector similarity"""
        
        if not self.vector_store:
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            retrieved = []
            
            for doc, score in results:
                similarity = 1 / (1 + score)
                retrieved.append({
                    'content': doc.page_content,
                    'source': doc.metadata.get('source', ''),
                    'candidate': doc.metadata.get('candidate', ''),
                    'score': similarity
                })
            
            return retrieved
        except Exception as e:
            st.error(f"Retrieval error: {str(e)}")
            return []
    
    def rerank_with_cohere(self, query: str, results: List[Dict]) -> List[Dict]:
        """Rerank results using Cohere"""
        
        if not self.cohere_client or not results:
            return results
        
        try:
            documents = [r['content'][:300] for r in results]
            
            response = self.cohere_client.rerank(
                model="rerank-english-v2.0",
                query=query,
                documents=documents,
                top_n=len(results)
            )
            
            reranked = []
            for rank in response.results:
                original = results[rank.index]
                original['rerank_score'] = rank.relevance_score
                reranked.append(original)
            
            return reranked
        except Exception as e:
            st.warning(f"Reranking failed: {str(e)}")
            return results

# =====================================================================
# COHERE GENERATION
# =====================================================================

def generate_answer_with_cohere(question: str, context: str) -> str:
    """Generate answer using Cohere Chat API"""
    
    if not COHERE_API_KEY:
        return "Cohere API key not configured"
    
    try:
        client = cohere.Client(COHERE_API_KEY)
        
        prompt = f"""You are an expert HR assistant helping find the best candidates.

Context (Candidate Information):
{context}

Question: {question}

Provide a helpful, professional response based on the candidate information provided."""
        
        response = client.chat(
            message=prompt,
            model="command-a-03-2025"
        )
        
        return response.text.strip()
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# =====================================================================
# SESSION INITIALIZATION
# =====================================================================

def init_session():
    """Initialize session state"""
    if 'retriever' not in st.session_state:
        st.session_state.retriever = ResumeRetriever()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'selected_resume' not in st.session_state:
        st.session_state.selected_resume = None

# =====================================================================
# UI COMPONENTS
# =====================================================================

def show_header():
    """Display professional header with neon styling"""
    st.markdown("""
    <h1 class="main-header">HR-CHATBOT</h1>
    <p class="subtitle">Advanced Candidate Intelligence Platform | AI-Powered Resume Analysis & Search</p>
    """, unsafe_allow_html=True)

def chatbot_tab():
    """Chatbot interface"""
    st.markdown("### Ask About Candidates")
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for msg, is_user in st.session_state.messages:
            if is_user:
                st.markdown(f'<div class="user-message"><strong>You:</strong> {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><strong>HR-Bot:</strong> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="empty-state">
            <p>Start a conversation about candidates. Ask about skills, experience, or find the perfect fit!</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
    user_input = st.text_input(
        "Type your question:",
        placeholder="e.g., 'Find Python developers with 5+ years of experience'",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        pass
    
    with col2:
        if st.button("SEARCH", use_container_width=True):
            if user_input:
                st.session_state.messages.append((user_input, True))
                
                with st.spinner("🔍 Searching candidates..."):
                    # Retrieve and rerank
                    results = st.session_state.retriever.retrieve(user_input)
                    reranked = st.session_state.retriever.rerank_with_cohere(user_input, results)
                    
                    # Generate answer
                    context = "\n".join([f"- {r['candidate']}: {r['content'][:200]}" for r in reranked])
                    answer = generate_answer_with_cohere(user_input, context)
                    
                    st.session_state.messages.append((answer, False))
                    
                    # Display answer
                    st.markdown(f'<div class="info-box"><strong>Answer:</strong><br/>{answer}</div>', unsafe_allow_html=True)
                    
                    # Display sources
                    if reranked:
                        st.markdown("#### Top Candidates")
                        for idx, result in enumerate(reranked, 1):
                            score = result.get('rerank_score', result.get('score', 0))
                            st.markdown(f'''
                            <div class="source-badge">
                                <strong>#{idx} - {result['candidate']}</strong><br/>
                                Relevance: <span style="color: #00f5ff; font-weight: bold;">{score:.0%}</span>
                            </div>
                            ''', unsafe_allow_html=True)
                
                st.rerun()

def browse_tab():
    """Browse and filter resumes"""
    st.markdown("### Browse Candidates")
    
    resumes = get_all_resumes()
    
    if resumes:
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Filter by name or skill:", placeholder="Search candidates...")
        with col2:
            st.markdown("#### Total Candidates")
            st.markdown(f'<div class="metric-box"><div class="metric-value">{len(resumes)}</div></div>', unsafe_allow_html=True)
        
        # Filter results
        filtered = [r for r in resumes if not search_term or search_term.lower() in r.get('candidate_name', '').lower()]
        
        if filtered:
            for resume in filtered:
                st.markdown('<div class="resume-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"#### {resume['candidate_name']}")
                    
                    metadata = {}
                    try:
                        if resume.get('metadata'):
                            metadata = json.loads(resume['metadata'])
                    except:
                        pass
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if resume.get('email'):
                            st.markdown(f"**Email:** {resume['email']}")
                        if resume.get('phone'):
                            st.markdown(f"**Phone:** {resume['phone']}")
                    
                    with col_b:
                        if resume.get('location'):
                            st.markdown(f"**Location:** {resume['location']}")
                        if metadata.get('experience_years'):
                            st.markdown(f"**Experience:** {metadata['experience_years']}+ years")
                
                with col2:
                    if st.button("View", key=f"view_{resume['resume_id']}", use_container_width=True):
                        st.session_state.selected_resume = resume
                
                with col3:
                    if st.button("Delete", key=f"delete_{resume['resume_id']}", use_container_width=True):
                        with sqlite3.connect(DB_PATH) as conn:
                            conn.execute("DELETE FROM resumes WHERE resume_id = ?", (resume['resume_id'],))
                            conn.commit()
                        st.success("Resume deleted!")
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("View Full Details"):
                    if metadata.get('skills'):
                        st.markdown(f"**Skills:** {', '.join(metadata['skills'])}")
                    if metadata.get('education'):
                        st.markdown(f"**Education:** {', '.join(metadata['education'])}")
                    st.markdown(f"**Added:** {resume.get('created_at', 'N/A')}")
        else:
            st.markdown('<div class="empty-state"><p>No candidates found</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="empty-state">
            <p>No resumes yet. Upload some to get started!</p>
        </div>
        ''', unsafe_allow_html=True)

def data_management_tab():
    """Manage resume data"""
    st.markdown("### Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Upload Resumes")
        uploaded_files = st.file_uploader("Choose PDF resume files", type=['pdf'], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Process & Index"):
                with st.spinner("Processing resumes..."):
                    try:
                        documents = []
                        
                        for uploaded_file in uploaded_files:
                            # Extract text from PDF
                            resume_text = extract_text_from_pdf(uploaded_file)
                            
                            if not resume_text.strip():
                                st.warning(f"Could not extract text from {uploaded_file.name}")
                                continue
                            
                            metadata = parse_resume(resume_text)
                            resume_id = hashlib.md5(resume_text[:100].encode()).hexdigest()
                            
                            # Extract candidate name from filename or text
                            candidate_name = uploaded_file.name.replace('.pdf', '').strip()
                            
                            # Try to extract name from resume text
                            lines = resume_text.split('\n')
                            for line in lines[:10]:
                                if len(line.strip()) > 2 and len(line.strip()) < 50 and not line.strip().isdigit():
                                    candidate_name = line.strip()
                                    break
                            
                            add_resume_to_db(resume_id, candidate_name, resume_text, metadata)
                            
                            documents.append({
                                'content': resume_text,
                                'source': resume_id,
                                'candidate_name': candidate_name
                            })
                        
                        if documents:
                            st.session_state.retriever.ingest(documents)
                            st.success(f"Successfully indexed {len(documents)} resumes!")
                            st.rerun()
                        else:
                            st.error("No valid resumes found")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("#### Database Statistics")
        resumes = get_all_resumes()
        st.markdown(f'''
        <div class="info-box">
            <strong>Total Resumes:</strong> {len(resumes)}<br/>
            <strong>Database:</strong> resumes.db<br/>
            <strong>Vector DB:</strong> ./chroma_db<br/>
            <strong>Format:</strong> PDF
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("Clear All Data"):
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("DELETE FROM resumes")
                conn.execute("DELETE FROM search_history")
                conn.commit()
            st.success("Database cleared!")
            st.rerun()

# =====================================================================
# MAIN APPLICATION
# =====================================================================

def main():
    init_database()
    init_session()
    
    show_header()
    
    tab1, tab2, tab3 = st.tabs(["Chatbot", "Browse", "Manage"])
    
    with tab1:
        chatbot_tab()
    
    with tab2:
        browse_tab()
    
    with tab3:
        data_management_tab()

if __name__ == "__main__":
    main()
