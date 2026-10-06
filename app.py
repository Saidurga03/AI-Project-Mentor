import os
import json
import textwrap
from datetime import datetime

import streamlit as st

# ============================================================
# DATABASE
# ============================================================

from database import (
    init_database,
    save_project,
    load_saved_projects,
    load_project,
    delete_project,
    get_project_count,
)

# ============================================================
# AI
# ============================================================

try:
    from services.ai_mentor import ask_mentor
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Project Mentor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

init_database()

# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "current_page": "🏠 Home",
    "selected_project": None,
    "saved_projects": [],
    "chat_history": [],
    "progress": 0,
    "completed_tasks": [],
    "tech_stack": [],
    "database_tables": [],
    "project_notes": "",
    "analysis_result": {},
    "presentation_content": "",
    "generated_report": "",
    "project_counter": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LOAD SAVED PROJECTS
# ============================================================

if not st.session_state.saved_projects:
    try:
        st.session_state.saved_projects = load_saved_projects()
    except Exception:
        st.session_state.saved_projects = []


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #f8f5ff 0%,
                #eef8ff 45%,
                #fff5f8 100%
            );
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #f1eaff,
                #eaf7ff,
                #fff1f6
            );
        border-right: 1px solid #ddd6fe;
    }

    .hero {
        padding: 35px;
        border-radius: 28px;
        background:
            linear-gradient(
                135deg,
                #e9ddff,
                #dff4ff,
                #ffe5ef
            );
        border: 1px solid #ded5f7;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(80, 60, 120, 0.10);
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
        color: #312e81;
    }

    .hero p {
        font-size: 18px;
        color: #475569;
    }

    .section-title {
        font-size: 30px;
        font-weight: 800;
        color: #312e81;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 22px;
    }

    .feature-card {
        padding: 22px;
        border-radius: 20px;
        background: rgba(255,255,255,0.78);
        border: 1px solid #e2e8f0;
        min-height: 150px;
        box-shadow: 0 7px 20px rgba(30, 41, 59, 0.06);
    }

    .feature-card h3 {
        color: #4338ca;
        margin-bottom: 8px;
    }

    .project-card {
        padding: 22px;
        border-radius: 22px;
        background: rgba(255,255,255,0.85);
        border: 1px solid #ddd6fe;
        box-shadow: 0 8px 25px rgba(30, 41, 59, 0.07);
        margin-bottom: 18px;
    }

    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        background: #ede9fe;
        color: #5b21b6;
        font-size: 13px;
        font-weight: 700;
        margin-right: 5px;
    }

    .ai-box {
        padding: 20px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #f1eaff,
            #e8f7ff
        );
        border: 1px solid #ddd6fe;
        margin: 15px 0;
    }

    .success-box {
        padding: 18px;
        border-radius: 18px;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
    }

    .small-muted {
        color: #64748b;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.75);
        border-radius: 18px;
        padding: 10px;
        border: 1px solid #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 50 PROJECTS
# ============================================================

PROJECT_LIBRARY = [

    {
        "name": "AI Resume Analyzer",
        "category": "🤖 Generative AI",
        "difficulty": "Intermediate",
        "description": "Analyze resumes using AI and provide skills, strengths, weaknesses, and improvement suggestions.",
        "problem": "Students and job seekers often struggle to understand whether their resume matches a target job.",
        "technologies": ["Python", "Streamlit", "LLM", "NLP", "PDF"],
        "libraries": ["Streamlit", "PyPDF2", "Groq", "Sentence Transformers"],
        "database": "SQLite",
        "features": [
            "Resume upload",
            "Skill extraction",
            "Job matching",
            "Resume scoring",
            "Improvement suggestions",
        ],
    },

    {
        "name": "AI Study Assistant",
        "category": "🎓 Education AI",
        "difficulty": "Intermediate",
        "description": "An AI assistant that helps students understand subjects, generate explanations, and create study plans.",
        "problem": "Students need personalized academic assistance outside classroom hours.",
        "technologies": ["Python", "Streamlit", "LLM", "NLP"],
        "libraries": ["Streamlit", "Groq", "Pandas"],
        "database": "SQLite",
        "features": [
            "AI tutor",
            "Study planner",
            "Question answering",
            "Topic explanations",
            "Progress tracking",
        ],
    },

    {
        "name": "AI Interview Preparation Assistant",
        "category": "💼 Career AI",
        "difficulty": "Intermediate",
        "description": "Generate interview questions and provide AI-powered feedback on candidate answers.",
        "problem": "Students often lack realistic interview practice.",
        "technologies": ["Python", "LLM", "NLP", "Streamlit"],
        "libraries": ["Streamlit", "Groq", "SpeechRecognition"],
        "database": "SQLite",
        "features": [
            "Technical questions",
            "HR questions",
            "Answer evaluation",
            "Interview scoring",
            "Improvement suggestions",
        ],
    },

    {
        "name": "AI Customer Support Chatbot",
        "category": "💬 Conversational AI",
        "difficulty": "Intermediate",
        "description": "Build an intelligent customer-support chatbot that answers questions using an organization's knowledge base.",
        "problem": "Businesses need automated customer support available at all times.",
        "technologies": ["Python", "LLM", "RAG", "NLP"],
        "libraries": ["LangChain", "Groq", "ChromaDB", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Chat interface",
            "Knowledge base",
            "FAQ answering",
            "Conversation history",
            "RAG search",
        ],
    },

    {
        "name": "AI Personal Productivity Assistant",
        "category": "🤖 Generative AI",
        "difficulty": "Intermediate",
        "description": "An AI assistant that helps users organize tasks, summarize information, and create productivity plans.",
        "problem": "Managing multiple tasks and priorities can be difficult.",
        "technologies": ["Python", "LLM", "NLP", "Streamlit"],
        "libraries": ["Streamlit", "Groq", "Pandas"],
        "database": "SQLite",
        "features": [
            "Task planning",
            "AI suggestions",
            "Daily planner",
            "Text summarization",
            "Priority management",
        ],
    },

    {
        "name": "AI Meeting Summarizer",
        "category": "🤖 Generative AI",
        "difficulty": "Intermediate",
        "description": "Convert meeting transcripts into concise summaries, decisions, and action items.",
        "problem": "Important meeting information can be difficult to review after long discussions.",
        "technologies": ["Python", "LLM", "NLP"],
        "libraries": ["Groq", "Streamlit", "Pandas"],
        "database": "SQLite",
        "features": [
            "Transcript upload",
            "Summary generation",
            "Action item extraction",
            "Decision extraction",
        ],
    },

    {
        "name": "AI Email Assistant",
        "category": "🤖 Generative AI",
        "difficulty": "Beginner",
        "description": "Generate professional email drafts from short user instructions.",
        "problem": "Writing professional emails can take significant time.",
        "technologies": ["Python", "LLM", "NLP"],
        "libraries": ["Streamlit", "Groq"],
        "database": "SQLite",
        "features": [
            "Email generation",
            "Tone selection",
            "Grammar improvement",
            "Email summarization",
        ],
    },

    {
        "name": "AI Code Explanation Assistant",
        "category": "💻 Developer AI",
        "difficulty": "Intermediate",
        "description": "Explain programming code in simple language and identify possible issues.",
        "problem": "Beginners often find complex source code difficult to understand.",
        "technologies": ["Python", "LLM", "NLP"],
        "libraries": ["Streamlit", "Groq"],
        "database": "SQLite",
        "features": [
            "Code explanation",
            "Bug detection",
            "Optimization suggestions",
            "Documentation generation",
        ],
    },

    {
        "name": "Sentiment Analysis System",
        "category": "🧠 NLP",
        "difficulty": "Beginner",
        "description": "Classify text as positive, negative, or neutral.",
        "problem": "Organizations need to understand customer opinions from large amounts of text.",
        "technologies": ["Python", "NLP", "Machine Learning"],
        "libraries": ["NLTK", "Scikit-learn", "Pandas"],
        "database": "SQLite",
        "features": [
            "Text classification",
            "Sentiment score",
            "Batch analysis",
            "Visualization",
        ],
    },

    {
        "name": "Fake News Detection System",
        "category": "📰 NLP",
        "difficulty": "Intermediate",
        "description": "Use machine learning and NLP techniques to classify news content.",
        "problem": "False information can spread rapidly through digital platforms.",
        "technologies": ["Python", "NLP", "Machine Learning"],
        "libraries": ["Scikit-learn", "NLTK", "Pandas"],
        "database": "SQLite",
        "features": [
            "News classification",
            "Text preprocessing",
            "Prediction score",
            "Dataset analysis",
        ],
    },

    {
        "name": "Text Summarization System",
        "category": "📝 NLP",
        "difficulty": "Intermediate",
        "description": "Generate short summaries from long documents.",
        "problem": "Reading large documents takes considerable time.",
        "technologies": ["Python", "NLP", "Transformers"],
        "libraries": ["Transformers", "Streamlit", "PyPDF2"],
        "database": "SQLite",
        "features": [
            "Document upload",
            "Automatic summary",
            "PDF support",
            "Summary length control",
        ],
    },

    {
        "name": "Spam Message Detector",
        "category": "🛡️ NLP",
        "difficulty": "Beginner",
        "description": "Classify messages as spam or legitimate.",
        "problem": "Users receive unwanted messages.",
        "technologies": ["Python", "NLP", "Machine Learning"],
        "libraries": ["Scikit-learn", "Pandas", "NLTK"],
        "database": "SQLite",
        "features": [
            "Spam classification",
            "Confidence score",
            "Batch prediction",
            "Dataset analytics",
        ],
    },

    {
        "name": "Resume Skill Extractor",
        "category": "💼 NLP",
        "difficulty": "Intermediate",
        "description": "Extract technical and soft skills automatically from resumes.",
        "problem": "Manually reviewing many resumes is time-consuming.",
        "technologies": ["Python", "NLP", "Machine Learning"],
        "libraries": ["spaCy", "PyPDF2", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Resume upload",
            "Skill extraction",
            "Skill categorization",
            "Candidate comparison",
        ],
    },

    {
        "name": "FAQ Question Answering System",
        "category": "💬 NLP",
        "difficulty": "Beginner",
        "description": "Answer frequently asked questions using a predefined knowledge base.",
        "problem": "Organizations repeatedly receive the same questions.",
        "technologies": ["Python", "NLP", "Semantic Search"],
        "libraries": ["Sentence Transformers", "Streamlit"],
        "database": "SQLite",
        "features": [
            "FAQ search",
            "Semantic similarity",
            "Question matching",
            "Answer ranking",
        ],
    },

    {
        "name": "Document Semantic Search Engine",
        "category": "🔎 NLP",
        "difficulty": "Intermediate",
        "description": "Search documents based on meaning rather than exact keywords.",
        "problem": "Traditional keyword search can miss semantically similar information.",
        "technologies": ["Python", "Embeddings", "NLP"],
        "libraries": ["Sentence Transformers", "ChromaDB"],
        "database": "SQLite + ChromaDB",
        "features": [
            "Document upload",
            "Vector search",
            "Semantic ranking",
            "Relevant passage retrieval",
        ],
    },

    {
        "name": "PDF RAG Chatbot",
        "category": "📄 RAG",
        "difficulty": "Advanced",
        "description": "Chat with PDF documents using retrieval-augmented generation.",
        "problem": "Users need to ask questions directly from large documents.",
        "technologies": ["Python", "RAG", "LLM", "Embeddings"],
        "libraries": ["ChromaDB", "Sentence Transformers", "PyPDF2", "Groq"],
        "database": "SQLite + ChromaDB",
        "features": [
            "PDF upload",
            "Document chunking",
            "Vector embeddings",
            "Semantic retrieval",
            "AI answers",
        ],
    },

    {
        "name": "College Knowledge RAG Assistant",
        "category": "🎓 RAG",
        "difficulty": "Advanced",
        "description": "A college information assistant that answers questions from college documents.",
        "problem": "Students struggle to find information across multiple documents.",
        "technologies": ["Python", "RAG", "LLM"],
        "libraries": ["ChromaDB", "Sentence Transformers", "Groq"],
        "database": "SQLite",
        "features": [
            "College document search",
            "AI question answering",
            "Citation support",
            "Document management",
        ],
    },

    {
        "name": "Research Paper RAG Assistant",
        "category": "📚 RAG",
        "difficulty": "Advanced",
        "description": "Search and question-answer over research papers using embeddings and LLMs.",
        "problem": "Researchers need to quickly locate information across long academic papers.",
        "technologies": ["Python", "RAG", "Embeddings", "LLM"],
        "libraries": ["ChromaDB", "Sentence Transformers", "PyPDF2"],
        "database": "SQLite + ChromaDB",
        "features": [
            "Paper upload",
            "Semantic search",
            "Question answering",
            "Research summaries",
        ],
    },

    {
        "name": "Student Performance Predictor",
        "category": "📊 Machine Learning",
        "difficulty": "Beginner",
        "description": "Predict student academic performance using historical student data.",
        "problem": "Educational institutions need early indicators of student performance.",
        "technologies": ["Python", "Machine Learning", "Data Science"],
        "libraries": ["Pandas", "Scikit-learn", "Matplotlib"],
        "database": "SQLite",
        "features": [
            "Student data",
            "Performance prediction",
            "Analytics dashboard",
            "Risk identification",
        ],
    },

    {
        "name": "House Price Prediction",
        "category": "🏠 Machine Learning",
        "difficulty": "Beginner",
        "description": "Predict property prices using location, area, rooms, and other features.",
        "problem": "Property prices depend on many interacting factors.",
        "technologies": ["Python", "Regression", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Price prediction",
            "Feature analysis",
            "Interactive form",
            "Visualization",
        ],
    },

    {
        "name": "Loan Approval Prediction",
        "category": "💰 Machine Learning",
        "difficulty": "Intermediate",
        "description": "Predict loan approval using applicant information.",
        "problem": "Financial institutions need efficient risk assessment systems.",
        "technologies": ["Python", "Classification", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Applicant analysis",
            "Approval prediction",
            "Risk score",
            "Data visualization",
        ],
    },

    {
        "name": "Customer Churn Prediction",
        "category": "📈 Machine Learning",
        "difficulty": "Intermediate",
        "description": "Predict which customers may stop using a service.",
        "problem": "Companies need to identify customers at risk of leaving.",
        "technologies": ["Python", "Classification", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Customer analysis",
            "Churn prediction",
            "Risk scoring",
            "Analytics dashboard",
        ],
    },

    {
        "name": "Employee Attrition Predictor",
        "category": "👨‍💼 Machine Learning",
        "difficulty": "Intermediate",
        "description": "Predict employee attrition using workplace and employee data.",
        "problem": "Organizations want to identify factors associated with employee turnover.",
        "technologies": ["Python", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Employee analysis",
            "Attrition prediction",
            "Risk factors",
            "Visualization",
        ],
    },

    {
        "name": "Sales Forecasting System",
        "category": "📊 Machine Learning",
        "difficulty": "Intermediate",
        "description": "Forecast future sales using historical sales data.",
        "problem": "Businesses need estimates of future demand.",
        "technologies": ["Python", "Time Series", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn", "Matplotlib"],
        "database": "SQLite",
        "features": [
            "Sales forecasting",
            "Trend analysis",
            "Charts",
            "Historical comparison",
        ],
    },

    {
        "name": "Customer Segmentation System",
        "category": "👥 Machine Learning",
        "difficulty": "Intermediate",
        "description": "Group customers according to behavior and purchasing patterns.",
        "problem": "Businesses need to understand different customer groups.",
        "technologies": ["Python", "Clustering", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Customer clustering",
            "Segment visualization",
            "Behavior analysis",
            "Marketing insights",
        ],
    },

    {
        "name": "Object Detection System",
        "category": "👁️ Computer Vision",
        "difficulty": "Advanced",
        "description": "Detect and identify objects in images and video.",
        "problem": "Automated visual object identification is useful in many systems.",
        "technologies": ["Python", "Computer Vision", "Deep Learning"],
        "libraries": ["OpenCV", "YOLO", "Ultralytics"],
        "database": "SQLite",
        "features": [
            "Image upload",
            "Object detection",
            "Bounding boxes",
            "Confidence scores",
        ],
    },

    {
        "name": "Face Recognition Attendance System",
        "category": "👤 Computer Vision",
        "difficulty": "Advanced",
        "description": "Automate attendance using computer vision-based identity recognition.",
        "problem": "Manual attendance takes time and can be difficult to manage.",
        "technologies": ["Python", "Computer Vision", "Deep Learning"],
        "libraries": ["OpenCV", "DeepFace"],
        "database": "SQLite",
        "features": [
            "Face detection",
            "Attendance recording",
            "Student database",
            "Attendance reports",
        ],
    },

    {
        "name": "Hand Gesture Recognition",
        "category": "✋ Computer Vision",
        "difficulty": "Intermediate",
        "description": "Recognize hand gestures using computer vision.",
        "problem": "Gesture-based interaction can provide alternative interfaces.",
        "technologies": ["Python", "Computer Vision", "Deep Learning"],
        "libraries": ["OpenCV", "MediaPipe"],
        "database": "SQLite",
        "features": [
            "Camera input",
            "Gesture detection",
            "Gesture classification",
            "Interactive controls",
        ],
    },

    {
        "name": "Emotion Recognition System",
        "category": "😊 Computer Vision",
        "difficulty": "Advanced",
        "description": "Classify visible facial expressions into broad emotion categories.",
        "problem": "Computer vision can be used to study visible facial-expression patterns.",
        "technologies": ["Python", "Computer Vision", "Deep Learning"],
        "libraries": ["OpenCV", "DeepFace"],
        "database": "SQLite",
        "features": [
            "Image analysis",
            "Expression classification",
            "Result visualization",
            "History",
        ],
    },

    {
        "name": "Image Classification System",
        "category": "🖼️ Computer Vision",
        "difficulty": "Intermediate",
        "description": "Classify uploaded images into predefined categories.",
        "problem": "Manual image classification becomes difficult with large datasets.",
        "technologies": ["Python", "Deep Learning", "Computer Vision"],
        "libraries": ["TensorFlow", "Keras", "OpenCV"],
        "database": "SQLite",
        "features": [
            "Image upload",
            "Prediction",
            "Confidence score",
            "Classification history",
        ],
    },

    {
        "name": "Crop Disease Detection",
        "category": "🌾 Agriculture AI",
        "difficulty": "Advanced",
        "description": "Identify possible crop diseases from leaf images.",
        "problem": "Early disease identification can help farmers respond more quickly.",
        "technologies": ["Python", "Deep Learning", "Computer Vision"],
        "libraries": ["TensorFlow", "Keras", "OpenCV"],
        "database": "SQLite",
        "features": [
            "Leaf image upload",
            "Disease classification",
            "Confidence score",
            "Basic recommendations",
        ],
    },

    {
        "name": "Smart Crop Recommendation",
        "category": "🌱 Agriculture AI",
        "difficulty": "Intermediate",
        "description": "Recommend crops based on soil and environmental characteristics.",
        "problem": "Choosing an appropriate crop can depend on multiple environmental factors.",
        "technologies": ["Python", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Soil data",
            "Weather inputs",
            "Crop recommendation",
            "Prediction history",
        ],
    },

    {
        "name": "Crop Yield Prediction",
        "category": "🌾 Agriculture AI",
        "difficulty": "Intermediate",
        "description": "Predict crop yield using historical agricultural data.",
        "problem": "Yield estimates can help with agricultural planning.",
        "technologies": ["Python", "Machine Learning", "Data Science"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Yield prediction",
            "Environmental analysis",
            "Historical trends",
            "Charts",
        ],
    },

    {
        "name": "Smart Irrigation Prediction",
        "category": "💧 Agriculture AI",
        "difficulty": "Intermediate",
        "description": "Predict irrigation requirements using environmental data.",
        "problem": "Efficient water management is important for agriculture.",
        "technologies": ["Python", "Machine Learning", "IoT"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Moisture analysis",
            "Irrigation prediction",
            "Sensor data",
            "Dashboard",
        ],
    },

    {
        "name": "Disease Risk Prediction",
        "category": "🏥 Healthcare AI",
        "difficulty": "Intermediate",
        "description": "Demonstration system that estimates disease risk from structured datasets.",
        "problem": "Machine learning can be studied for identifying patterns in health datasets.",
        "technologies": ["Python", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Dataset analysis",
            "Risk prediction",
            "Visualization",
            "Prediction history",
        ],
    },

    {
        "name": "Medical Report Summarizer",
        "category": "🏥 Healthcare AI",
        "difficulty": "Advanced",
        "description": "Summarize uploaded medical documents into easier-to-read information.",
        "problem": "Long documents can be difficult to review quickly.",
        "technologies": ["Python", "NLP", "LLM"],
        "libraries": ["PyPDF2", "Groq", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Document upload",
            "AI summarization",
            "Key information extraction",
            "History",
        ],
    },

    {
        "name": "Healthcare FAQ Assistant",
        "category": "🏥 Healthcare AI",
        "difficulty": "Intermediate",
        "description": "Answer general healthcare information questions using a controlled knowledge base.",
        "problem": "Users often need quick access to general health information.",
        "technologies": ["Python", "NLP", "RAG"],
        "libraries": ["ChromaDB", "Sentence Transformers", "Streamlit"],
        "database": "SQLite",
        "features": [
            "FAQ search",
            "Knowledge base",
            "Semantic search",
            "Source display",
        ],
    },

    {
        "name": "Phishing URL Detection",
        "category": "🔐 Cybersecurity AI",
        "difficulty": "Intermediate",
        "description": "Classify URLs using machine learning features to study phishing detection.",
        "problem": "Suspicious links can expose users to security risks.",
        "technologies": ["Python", "Machine Learning", "Cybersecurity"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "URL analysis",
            "Feature extraction",
            "Classification",
            "Risk score",
        ],
    },

    {
        "name": "Network Intrusion Detection",
        "category": "🛡️ Cybersecurity AI",
        "difficulty": "Advanced",
        "description": "Analyze network datasets and classify potentially abnormal traffic.",
        "problem": "Large networks generate too much traffic for simple manual analysis.",
        "technologies": ["Python", "Machine Learning", "Cybersecurity"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Traffic analysis",
            "Anomaly detection",
            "Classification",
            "Security dashboard",
        ],
    },

    {
        "name": "Password Strength Analyzer",
        "category": "🔐 Cybersecurity",
        "difficulty": "Beginner",
        "description": "Evaluate password strength using safe rule-based analysis.",
        "problem": "Users may choose passwords that are easy to guess.",
        "technologies": ["Python", "Cybersecurity"],
        "libraries": ["Streamlit"],
        "database": "SQLite",
        "features": [
            "Strength score",
            "Rule checking",
            "Security suggestions",
            "History without storing passwords",
        ],
    },

    {
        "name": "Spam Email Classifier",
        "category": "📧 Cybersecurity AI",
        "difficulty": "Beginner",
        "description": "Classify email text into spam and legitimate categories.",
        "problem": "Spam emails create noise and can sometimes contain suspicious content.",
        "technologies": ["Python", "NLP", "Machine Learning"],
        "libraries": ["Scikit-learn", "NLTK", "Pandas"],
        "database": "SQLite",
        "features": [
            "Email classification",
            "Confidence score",
            "Batch testing",
            "Analytics",
        ],
    },

    {
        "name": "Personal Expense Analyzer",
        "category": "💰 Finance AI",
        "difficulty": "Beginner",
        "description": "Analyze personal expenses and identify spending patterns.",
        "problem": "People often find it difficult to understand where their money goes.",
        "technologies": ["Python", "Data Analytics", "Machine Learning"],
        "libraries": ["Pandas", "Plotly", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Expense tracking",
            "Category analysis",
            "Charts",
            "Monthly reports",
        ],
    },

    {
        "name": "Stock Market Trend Analyzer",
        "category": "📈 Finance AI",
        "difficulty": "Intermediate",
        "description": "Analyze historical market data and visualize trends.",
        "problem": "Large amounts of financial data can be difficult to interpret.",
        "technologies": ["Python", "Data Science", "Machine Learning"],
        "libraries": ["Pandas", "Matplotlib", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Historical data",
            "Trend charts",
            "Technical indicators",
            "Analytics dashboard",
        ],
    },

    {
        "name": "Credit Risk Prediction",
        "category": "💳 Finance AI",
        "difficulty": "Advanced",
        "description": "Use machine learning to study credit-risk classification on a suitable dataset.",
        "problem": "Financial organizations need methods for assessing credit-risk patterns.",
        "technologies": ["Python", "Machine Learning", "Classification"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Risk classification",
            "Feature analysis",
            "Model evaluation",
            "Risk dashboard",
        ],
    },

    {
        "name": "Movie Recommendation System",
        "category": "🎬 Recommendation AI",
        "difficulty": "Intermediate",
        "description": "Recommend movies based on user preferences and similarity.",
        "problem": "Users need help discovering relevant content from large catalogs.",
        "technologies": ["Python", "Recommendation Systems", "Machine Learning"],
        "libraries": ["Pandas", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Movie search",
            "Recommendations",
            "Similarity scoring",
            "User preferences",
        ],
    },

    {
        "name": "Book Recommendation System",
        "category": "📚 Recommendation AI",
        "difficulty": "Intermediate",
        "description": "Recommend books based on genres, descriptions, and preferences.",
        "problem": "Readers may struggle to discover books matching their interests.",
        "technologies": ["Python", "NLP", "Recommendation Systems"],
        "libraries": ["Pandas", "Scikit-learn", "Sentence Transformers"],
        "database": "SQLite",
        "features": [
            "Book search",
            "Similar books",
            "Genre filtering",
            "Recommendation history",
        ],
    },

    {
        "name": "Job Recommendation System",
        "category": "💼 Recommendation AI",
        "difficulty": "Advanced",
        "description": "Recommend job opportunities based on skills and preferences.",
        "problem": "Job seekers face thousands of listings and need relevant opportunities.",
        "technologies": ["Python", "NLP", "Recommendation Systems"],
        "libraries": ["Pandas", "Scikit-learn", "Sentence Transformers"],
        "database": "SQLite",
        "features": [
            "Skill matching",
            "Job recommendations",
            "Similarity scoring",
            "Profile management",
        ],
    },

    {
        "name": "Speech-to-Text Assistant",
        "category": "🎤 Speech AI",
        "difficulty": "Intermediate",
        "description": "Convert spoken language into text and use the result in an AI assistant.",
        "problem": "Voice input can make applications easier to interact with.",
        "technologies": ["Python", "Speech AI", "NLP"],
        "libraries": ["SpeechRecognition", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Voice input",
            "Text conversion",
            "AI processing",
            "History",
        ],
    },

    {
        "name": "AI Voice Notes Assistant",
        "category": "🎙️ Speech AI",
        "difficulty": "Intermediate",
        "description": "Record spoken notes and convert them into organized text.",
        "problem": "Typing notes manually can be inconvenient.",
        "technologies": ["Python", "Speech Recognition", "NLP"],
        "libraries": ["SpeechRecognition", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Voice notes",
            "Transcription",
            "Note organization",
            "Search",
        ],
    },

    {
        "name": "AI Quiz Generator",
        "category": "🎓 Education AI",
        "difficulty": "Intermediate",
        "description": "Generate quizzes automatically from topics or uploaded study material.",
        "problem": "Creating personalized practice questions manually takes time.",
        "technologies": ["Python", "LLM", "NLP"],
        "libraries": ["Groq", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Question generation",
            "Multiple choice questions",
            "Difficulty selection",
            "Score tracking",
        ],
    },

    {
        "name": "Personalized Learning Recommendation System",
        "category": "🎓 Education AI",
        "difficulty": "Advanced",
        "description": "Recommend learning resources based on student performance.",
        "problem": "Students have different learning needs and progress levels.",
        "technologies": ["Python", "Machine Learning", "Recommendation Systems"],
        "libraries": ["Pandas", "Scikit-learn", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Student profiles",
            "Performance analysis",
            "Resource recommendations",
            "Progress tracking",
        ],
    },

    {
        "name": "AI Programming Tutor",
        "category": "💻 Education AI",
        "difficulty": "Advanced",
        "description": "An AI tutor that explains programming concepts and helps students understand code.",
        "problem": "Programming beginners often need personalized explanations.",
        "technologies": ["Python", "LLM", "NLP"],
        "libraries": ["Groq", "Streamlit"],
        "database": "SQLite",
        "features": [
            "Programming questions",
            "Code explanation",
            "Examples",
            "Learning history",
        ],
    },

    {
        "name": "Business Analytics Assistant",
        "category": "📊 Business AI",
        "difficulty": "Intermediate",
        "description": "Analyze business datasets and generate natural-language insights.",
        "problem": "Non-technical users may find data analysis difficult.",
        "technologies": ["Python", "LLM", "Data Analytics"],
        "libraries": ["Pandas", "Streamlit", "Groq"],
        "database": "SQLite",
        "features": [
            "CSV upload",
            "Automatic analysis",
            "Charts",
            "AI insights",
        ],
    },

    {
        "name": "Customer Feedback Analyzer",
        "category": "📊 Business AI",
        "difficulty": "Intermediate",
        "description": "Analyze customer feedback using sentiment and topic analysis.",
        "problem": "Businesses receive large volumes of feedback that are difficult to review manually.",
        "technologies": ["Python", "NLP", "Machine Learning"],
        "libraries": ["Pandas", "NLTK", "Scikit-learn"],
        "database": "SQLite",
        "features": [
            "Feedback upload",
            "Sentiment analysis",
            "Topic analysis",
            "Dashboard",
        ],
    },

    {
        "name": "AI Project Mentor Platform",
        "category": "🚀 Full-Stack AI",
        "difficulty": "Advanced",
        "description": "An intelligent platform that helps students plan, analyze, build, test, document, and present AI/ML projects.",
        "problem": "Students often struggle to manage the complete lifecycle of an AI project.",
        "technologies": [
            "Python",
            "Streamlit",
            "LLM",
            "NLP",
            "Machine Learning",
            "SQLite",
            "RAG",
        ],
        "libraries": [
            "Streamlit",
            "Groq",
            "Pandas",
            "Scikit-learn",
            "Sentence Transformers",
            "ChromaDB",
        ],
        "database": "SQLite + ChromaDB",
        "features": [
            "Project ideas",
            "Project analyzer",
            "Technology recommendations",
            "Database designer",
            "Project roadmap",
            "Progress tracking",
            "AI mentor",
            "Code assistant",
            "Bug explainer",
            "Presentation assistant",
            "Project report generator",
        ],
    },
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_project_name(project):
    if not project:
        return "Untitled Project"

    return project.get(
        "name",
        project.get("title", "Untitled Project")
    )


def project_value(key, default=""):
    project = st.session_state.selected_project

    if not project:
        return default

    return project.get(key, default)


def navigate(page):
    st.session_state.current_page = page
    st.rerun()


def save_current_project():
    project = st.session_state.selected_project

    if not project:
        return

    try:
        save_project(
            project=project,
            progress=int(st.session_state.progress),
            completed_tasks=st.session_state.completed_tasks,
            tech_stack=st.session_state.tech_stack,
            database_tables=st.session_state.database_tables,
            project_notes=st.session_state.project_notes,
        )

        st.session_state.saved_projects = load_saved_projects()

    except Exception as error:
        st.error(f"Could not save project: {error}")


def select_project(project):

    st.session_state.selected_project = project

    st.session_state.progress = 0
    st.session_state.completed_tasks = []
    st.session_state.tech_stack = project.get(
        "technologies", []
    ).copy()
    st.session_state.database_tables = []
    st.session_state.project_notes = ""
    st.session_state.analysis_result = {}

    existing = load_project(
        get_project_name(project)
    )

    if existing:

        st.session_state.progress = existing.get(
            "progress", 0
        )

        st.session_state.completed_tasks = existing.get(
            "completed_tasks", []
        )

        st.session_state.tech_stack = existing.get(
            "tech_stack",
            project.get("technologies", [])
        )

        st.session_state.database_tables = existing.get(
            "database_tables", []
        )

        st.session_state.project_notes = existing.get(
            "project_notes", ""
        )

    save_current_project()


def search_projects(query):

    query = query.strip().lower()

    if not query:
        return PROJECT_LIBRARY

    results = []

    for project in PROJECT_LIBRARY:

        searchable = " ".join(
            [
                project.get("name", ""),
                project.get("category", ""),
                project.get("description", ""),
                project.get("problem", ""),
                " ".join(project.get("technologies", [])),
                " ".join(project.get("features", [])),
            ]
        ).lower()

        if query in searchable:
            results.append(project)

    return results


def project_categories():
    return sorted(
        list(
            set(
                project["category"]
                for project in PROJECT_LIBRARY
            )
        )
    )


def current_project_exists():
    return st.session_state.selected_project is not None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
        ">
            <div style="font-size:42px;">🤖</div>
            <h2 style="color:#4338ca;">AI Project Mentor</h2>
            <p style="color:#64748b;">
                Build smarter projects.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    pages = [
        "🏠 Home",
        "📊 Dashboard",
        "💡 Project Ideas",
        "📁 My Projects",
        "🧠 Project Analyzer",
        "🗺️ Project Roadmap",
        "🛠️ Technology Stack",
        "🗄️ Database Designer",
        "📚 Resources",
        "📈 Progress Tracker",
        "🧪 Testing Assistant",
        "🤖 AI Mentor",
        "💻 AI Code Assistant",
        "🐛 Bug Explainer",
        "🎤 Presentation Assistant",
        "📝 Project Report",
        "⚙️ Settings",
    ]

    current_index = (
        pages.index(st.session_state.current_page)
        if st.session_state.current_page in pages
        else 0
    )

    selected_page = st.radio(
        "Navigation",
        pages,
        index=current_index,
        key="main_navigation",
    )

    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    st.divider()

    if current_project_exists():

        st.markdown("### 📌 Current Project")

        st.info(
            get_project_name(
                st.session_state.selected_project
            )
        )

        st.progress(
            st.session_state.progress / 100
        )

        st.caption(
            f"{st.session_state.progress}% completed"
        )

    else:

        st.caption(
            "No project selected yet."
        )

    st.divider()

    st.caption(
        f"📁 {get_project_count()} saved project(s)"
    )


# ============================================================
# HOME
# ============================================================

def render_home():

    st.title("🤖 AI Project Mentor")
    st.subheader("Turn Your Ideas Into Intelligent Projects.")
    st.write(
        "Plan, analyze, build, test, document and present "
        "your AI/ML projects from one intelligent workspace."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🚀 Projects", len(PROJECT_LIBRARY))

    with col2:
        st.metric("📂 Categories", len(project_categories()))

    with col3:
        st.metric("💾 Saved", get_project_count())

    with col4:
        st.metric("🧠 AI Tools", "7+")

    st.markdown("## ✨ What can you build?")
    st.write(
        "Everything you need to move from an idea to a complete project."
    )

    features = [
        ("💡", "Project Ideas", "Explore 50+ AI/ML project ideas."),
        ("🧠", "Project Analyzer", "Understand feasibility, complexity and technologies."),
        ("🗺️", "Project Roadmap", "Break your project into practical development stages."),
        ("🛠️", "Technology Stack", "Choose languages, frameworks, libraries and tools."),
        ("🗄️", "Database Designer", "Design database tables for your application."),
        ("📈", "Progress Tracker", "Track completed tasks and project progress."),
        ("🤖", "AI Mentor", "Ask AI for project-development guidance."),
        ("📝", "Project Report", "Generate a structured project report."),
    ]

    for start in range(0, len(features), 4):
        cols = st.columns(4)
        for i, feature in enumerate(features[start:start + 4]):
            with cols[i]:
                icon, title, description = feature
                st.markdown(f"**{icon} {title}**")
                st.caption(description)

    st.markdown("## 🚀 Start Building")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "💡 Explore 50 Project Ideas",
            use_container_width=True,
        ):
            navigate("💡 Project Ideas")

    with col2:
        if st.button(
            "📁 Open My Projects",
            use_container_width=True,
        ):
            navigate("📁 My Projects")



# ============================================================
# DASHBOARD
# ============================================================

def render_dashboard():

    st.markdown(
        '<div class="section-title">📊 Project Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your AI project workspace at a glance.'
        '</div>',
        unsafe_allow_html=True,
    )

    saved = load_saved_projects()

    total_projects = len(saved)

    average_progress = 0

    if saved:

        average_progress = int(
            sum(
                item.get("progress", 0)
                for item in saved
            ) / len(saved)
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📁 Saved Projects",
            total_projects
        )

    with col2:
        st.metric(
            "📈 Average Progress",
            f"{average_progress}%"
        )

    with col3:
        st.metric(
            "💡 Available Ideas",
            len(PROJECT_LIBRARY)
        )

    with col4:
        st.metric(
            "🛠️ Categories",
            len(project_categories())
        )

    st.divider()

    if not saved:

        st.info(
            "You haven't saved a project yet."
        )

        if st.button("💡 Explore Project Ideas"):
            navigate("💡 Project Ideas")

        return

    st.markdown("### 📌 Your Projects")

    for item in saved[:8]:

        project = item["project"]

        name = get_project_name(project)
        progress = item.get("progress", 0)

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### {name}"
                )

                st.caption(
                    f"{project.get('category', 'AI/ML')} • "
                    f"{project.get('difficulty', 'Intermediate')}"
                )

            with col2:

                st.progress(
                    progress / 100
                )

                st.caption(
                    f"{progress}% complete"
                )

            with col3:

                if st.button(
                    "Open",
                    key=f"dashboard_open_{name}"
                ):

                    select_project(project)
                    navigate("📁 My Projects")


# ============================================================
# PROJECT IDEAS
# ============================================================

def render_project_ideas():

    st.markdown(
        '<div class="section-title">💡 AI & ML Project Library</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Explore 50 projects across AI, ML, NLP, RAG, computer vision, '
        'cybersecurity, healthcare, agriculture and more.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🚀 Projects",
            len(PROJECT_LIBRARY)
        )

    with col2:
        st.metric(
            "📂 Categories",
            len(project_categories())
        )

    with col3:
        st.metric(
            "🌱 Beginner",
            len([
                p for p in PROJECT_LIBRARY
                if p["difficulty"] == "Beginner"
            ])
        )

    with col4:
        st.metric(
            "🔥 Advanced",
            len([
                p for p in PROJECT_LIBRARY
                if p["difficulty"] == "Advanced"
            ])
        )

    st.divider()

    search = st.text_input(
        "🔎 Search projects",
        placeholder="Try: chatbot, agriculture, computer vision, NLP..."
    )

    category_options = [
        "All Categories"
    ] + project_categories()

    selected_category = st.selectbox(
        "📂 Category",
        category_options
    )

    difficulty_options = [
        "All Levels",
        "Beginner",
        "Intermediate",
        "Advanced",
    ]

    selected_difficulty = st.selectbox(
        "🎯 Difficulty",
        difficulty_options
    )

    projects = search_projects(search)

    if selected_category != "All Categories":

        projects = [
            p for p in projects
            if p["category"] == selected_category
        ]

    if selected_difficulty != "All Levels":

        projects = [
            p for p in projects
            if p["difficulty"] == selected_difficulty
        ]

    st.markdown(
        f"### Showing {len(projects)} project(s)"
    )

    if not projects:

        st.warning(
            "No projects matched your search."
        )

        return

    for index, project in enumerate(projects):

        with st.container(border=True):

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.markdown(
                    f"## {project['name']}"
                )

                st.caption(
                    f"{project['category']} • "
                    f"{project['difficulty']}"
                )

                st.write(
                    project["description"]
                )

                st.markdown("**Problem:**")

                st.write(
                    project["problem"]
                )

            with col2:

                st.markdown(
                    "### 🛠️ Stack"
                )

                for technology in project[
                    "technologies"
                ]:

                    st.markdown(
                        f"- {technology}"
                    )

            with st.expander(
                "🔍 View Project Details"
            ):

                st.markdown(
                    "**Python Libraries**"
                )

                st.write(
                    ", ".join(
                        project["libraries"]
                    )
                )

                st.markdown(
                    "**Database**"
                )

                st.write(
                    project["database"]
                )

                st.markdown(
                    "**Key Features**"
                )

                for feature in project["features"]:

                    st.markdown(
                        f"✓ {feature}"
                    )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🚀 Use This Project",
                    key=f"use_{index}_{project['name']}",
                    use_container_width=True,
                ):

                    select_project(project)

                    st.success(
                        f"{project['name']} saved successfully!"
                    )

                    navigate("📁 My Projects")

            with col2:

                if st.button(
                    "🧠 Analyze",
                    key=f"analyze_{index}_{project['name']}",
                    use_container_width=True,
                ):

                    select_project(project)

                    navigate("🧠 Project Analyzer")


# ============================================================
# MY PROJECTS
# ============================================================

def render_my_projects():

    st.markdown(
        '<div class="section-title">📁 My Projects</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Your projects are stored permanently in SQLite.'
        '</div>',
        unsafe_allow_html=True,
    )

    projects = load_saved_projects()

    if not projects:

        st.info(
            "No saved projects yet."
        )

        if st.button(
            "💡 Browse Project Library"
        ):

            navigate("💡 Project Ideas")

        return

    st.metric(
        "💾 Saved Projects",
        len(projects)
    )

    st.divider()

    for index, item in enumerate(projects):

        project = item["project"]

        name = get_project_name(project)

        progress = item.get(
            "progress",
            0
        )

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### 📁 {name}"
                )

                st.caption(
                    f"{project.get('category', '')} • "
                    f"{project.get('difficulty', '')}"
                )

            with col2:

                st.progress(
                    progress / 100
                )

                st.caption(
                    f"{progress}% complete"
                )

            with col3:

                if st.button(
                    "Open",
                    key=f"open_saved_{index}"
                ):

                    select_project(project)

                    # Restore database state
                    loaded = load_project(name)

                    if loaded:

                        st.session_state.progress = loaded.get(
                            "progress",
                            0
                        )

                        st.session_state.completed_tasks = loaded.get(
                            "completed_tasks",
                            []
                        )

                        st.session_state.tech_stack = loaded.get(
                            "tech_stack",
                            project.get("technologies", [])
                        )

                        st.session_state.database_tables = loaded.get(
                            "database_tables",
                            []
                        )

                        st.session_state.project_notes = loaded.get(
                            "project_notes",
                            ""
                        )

                    st.rerun()

            with st.expander(
                "Project Information"
            ):

                st.write(
                    project.get(
                        "description",
                        ""
                    )
                )

                st.write(
                    "**Technologies:** "
                    + ", ".join(
                        project.get(
                            "technologies",
                            []
                        )
                    )
                )

                st.write(
                    "**Features:** "
                    + ", ".join(
                        project.get(
                            "features",
                            []
                        )
                    )
                )

            delete_col, duplicate_col = st.columns(2)

            with delete_col:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{index}"
                ):

                    if delete_project(name):

                        if (
                            st.session_state.selected_project
                            and get_project_name(
                                st.session_state.selected_project
                            ) == name
                        ):

                            st.session_state.selected_project = None

                        st.session_state.saved_projects = load_saved_projects()

                        st.success(
                            "Project deleted."
                        )

                        st.rerun()

            with duplicate_col:

                if st.button(
                    "📋 Duplicate",
                    key=f"duplicate_{index}"
                ):

                    duplicate = project.copy()

                    duplicate["name"] = (
                        f"{name} Copy"
                    )

                    save_project(
                        duplicate,
                        progress=0,
                        completed_tasks=[],
                        tech_stack=duplicate.get(
                            "technologies",
                            []
                        ),
                        database_tables=[],
                        project_notes="",
                    )

                    st.success(
                        "Project duplicated."
                    )

                    st.rerun()


# ============================================================
# PROJECT ANALYZER
# ============================================================

def render_project_analyzer():

    st.markdown(
        '<div class="section-title">🧠 Project Analyzer</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project from Project Ideas first."
        )

        return

    project = st.session_state.selected_project

    st.markdown(
        f"## {get_project_name(project)}"
    )

    st.write(
        project.get(
            "description",
            ""
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Difficulty",
            project.get(
                "difficulty",
                "Intermediate"
            )
        )

    with col2:
        st.metric(
            "Technologies",
            len(
                project.get(
                    "technologies",
                    []
                )
            )
        )

    with col3:
        st.metric(
            "Features",
            len(
                project.get(
                    "features",
                    []
                )
            )
        )

    st.divider()

    st.markdown("### 🎯 Problem Statement")

    st.info(
        project.get(
            "problem",
            "No problem statement available."
        )
    )

    st.markdown("### 🛠️ Recommended Technologies")

    cols = st.columns(
        min(
            4,
            len(
                project.get(
                    "technologies",
                    []
                )
            )
        )
    )

    for i, technology in enumerate(
        project.get(
            "technologies",
            []
        )
    ):

        with cols[i % len(cols)]:
            st.success(
                technology
            )

    st.markdown("### ✨ Key Features")

    for feature in project.get(
        "features",
        []
    ):

        st.checkbox(
            feature,
            value=feature in st.session_state.completed_tasks,
            key=f"analyzer_feature_{feature}",
        )

    st.markdown("### 📚 Recommended Libraries")

    st.write(
        ", ".join(
            project.get(
                "libraries",
                []
            )
        )
    )

    st.markdown("### 🗄️ Recommended Database")

    st.info(
        project.get(
            "database",
            "SQLite"
        )
    )


# ============================================================
# ROADMAP
# ============================================================

def render_roadmap():

    st.markdown(
        '<div class="section-title">🗺️ Project Roadmap</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project_name = get_project_name(
        st.session_state.selected_project
    )

    st.markdown(
        f"## 🚀 {project_name}"
    )

    roadmap = [
        (
            "1",
            "💡 Idea & Requirements",
            "Define the problem, users, objectives and expected output."
        ),
        (
            "2",
            "📊 Dataset & Research",
            "Collect, clean and understand the required data."
        ),
        (
            "3",
            "🧠 AI/ML Design",
            "Choose the model, algorithms, embeddings or LLM approach."
        ),
        (
            "4",
            "💻 Development",
            "Build the backend, interface and AI functionality."
        ),
        (
            "5",
            "🗄️ Database",
            "Create tables and connect persistent application data."
        ),
        (
            "6",
            "🧪 Testing",
            "Test functionality, accuracy, usability and edge cases."
        ),
        (
            "7",
            "📈 Evaluation",
            "Measure model and application performance."
        ),
        (
            "8",
            "📝 Documentation",
            "Prepare README, diagrams, report and presentation."
        ),
        (
            "9",
            "🚀 Deployment",
            "Deploy the completed project and prepare demonstration."
        ),
    ]

    for number, title, description in roadmap:

        with st.container(border=True):

            st.markdown(
                f"### {number}. {title}"
            )

            st.write(
                description
            )


# ============================================================
# TECHNOLOGY STACK
# ============================================================

def render_technology_stack():

    st.markdown(
        '<div class="section-title">🛠️ Technology Stack</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project = st.session_state.selected_project

    st.markdown(
        f"## {get_project_name(project)}"
    )

    default_stack = project.get(
        "technologies",
        []
    )

    selected = st.multiselect(
        "Select technologies",
        [
            "Python",
            "Streamlit",
            "Flask",
            "Django",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "LLM",
            "RAG",
            "Computer Vision",
            "OpenCV",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "Groq",
            "ChromaDB",
            "Sentence Transformers",
            "SQLite",
            "PostgreSQL",
            "MySQL",
            "HTML",
            "CSS",
            "JavaScript",
            "Git",
            "Docker",
        ],
        default=[
            x for x in default_stack
            if x in [
                "Python",
                "Streamlit",
                "Flask",
                "Django",
                "Machine Learning",
                "Deep Learning",
                "NLP",
                "LLM",
                "RAG",
                "Computer Vision",
                "OpenCV",
                "TensorFlow",
                "PyTorch",
                "Scikit-learn",
                "Pandas",
                "NumPy",
                "Groq",
                "ChromaDB",
                "Sentence Transformers",
                "SQLite",
                "PostgreSQL",
                "MySQL",
                "HTML",
                "CSS",
                "JavaScript",
                "Git",
                "Docker",
            ]
        ],
    )

    st.session_state.tech_stack = selected

    if st.button(
        "💾 Save Technology Stack"
    ):

        save_current_project()

        st.success(
            "Technology stack saved."
        )

    st.markdown("### Current Stack")

    for technology in selected:

        st.success(
            f"✓ {technology}"
        )


# ============================================================
# DATABASE DESIGNER
# ============================================================

def render_database_designer():

    st.markdown(
        '<div class="section-title">🗄️ Database Designer</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    st.markdown(
        "### Create Database Tables"
    )

    table_name = st.text_input(
        "Table name",
        placeholder="students"
    )

    columns_text = st.text_area(
        "Columns",
        placeholder=(
            "id INTEGER PRIMARY KEY\n"
            "name TEXT\n"
            "email TEXT\n"
            "created_at TEXT"
        ),
    )

    if st.button(
        "➕ Add Table"
    ):

        if table_name.strip():

            table = {
                "name": table_name.strip(),
                "columns": [
                    line.strip()
                    for line in columns_text.splitlines()
                    if line.strip()
                ],
            }

            st.session_state.database_tables.append(
                table
            )

            save_current_project()

            st.success(
                f"Table '{table_name}' added."
            )

    st.divider()

    if not st.session_state.database_tables:

        st.info(
            "No tables created yet."
        )

        return

    st.markdown(
        "### 📋 Current Tables"
    )

    for index, table in enumerate(
        st.session_state.database_tables
    ):

        with st.container(border=True):

            st.markdown(
                f"### 🗄️ {table['name']}"
            )

            for column in table.get(
                "columns",
                []
            ):

                st.code(
                    column
                )

            if st.button(
                "🗑️ Remove Table",
                key=f"remove_table_{index}"
            ):

                st.session_state.database_tables.pop(
                    index
                )

                save_current_project()

                st.rerun()


# ============================================================
# RESOURCES
# ============================================================

def render_resources():

    st.markdown(
        '<div class="section-title">📚 Resources</div>',
        unsafe_allow_html=True,
    )

    resources = [
        (
            "🐍 Python",
            "Programming language for AI/ML development."
        ),
        (
            "📊 Pandas",
            "Data manipulation and analysis."
        ),
        (
            "🧠 Scikit-learn",
            "Classical machine learning algorithms."
        ),
        (
            "👁️ OpenCV",
            "Computer vision and image processing."
        ),
        (
            "🔤 Sentence Transformers",
            "Text embeddings and semantic similarity."
        ),
        (
            "🗃️ ChromaDB",
            "Vector database for retrieval applications."
        ),
        (
            "🤖 LLMs",
            "Large language models for generative AI."
        ),
        (
            "🎈 Streamlit",
            "Rapid Python application development."
        ),
    ]

    for start in range(
        0,
        len(resources),
        2
    ):

        cols = st.columns(2)

        for i, resource in enumerate(
            resources[start:start + 2]
        ):

            with cols[i]:

                title, description = resource

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {title}"
                    )

                    st.write(
                        description
                    )


# ============================================================
# PROGRESS TRACKER
# ============================================================

def render_progress_tracker():

    st.markdown(
        '<div class="section-title">📈 Progress Tracker</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project = st.session_state.selected_project

    st.markdown(
        f"## {get_project_name(project)}"
    )

    progress = st.slider(
        "Overall project progress",
        min_value=0,
        max_value=100,
        value=int(
            st.session_state.progress
        ),
        step=5,
    )

    st.session_state.progress = progress

    st.progress(
        progress / 100
    )

    st.markdown(
        f"### {progress}% Complete"
    )

    tasks = [
        "Define project problem",
        "Research existing solutions",
        "Collect dataset",
        "Clean dataset",
        "Design AI/ML approach",
        "Build backend",
        "Build user interface",
        "Connect database",
        "Integrate AI model",
        "Test application",
        "Evaluate results",
        "Prepare documentation",
        "Prepare presentation",
        "Deploy project",
    ]

    st.markdown(
        "### ✅ Project Tasks"
    )

    completed = []

    for index, task in enumerate(tasks):

        checked = st.checkbox(
            task,
            value=task in st.session_state.completed_tasks,
            key=f"progress_task_{index}",
        )

        if checked:
            completed.append(task)

    st.session_state.completed_tasks = completed

    if st.button(
        "💾 Save Progress",
        use_container_width=True,
    ):

        save_current_project()

        st.success(
            "Progress saved to SQLite."
        )


# ============================================================
# TESTING ASSISTANT
# ============================================================

def render_testing_assistant():

    st.markdown(
        '<div class="section-title">🧪 Testing Assistant</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project = st.session_state.selected_project

    st.markdown(
        f"## Testing: {get_project_name(project)}"
    )

    test_cases = [
        "Application starts without errors",
        "User input validation works",
        "Database connection works",
        "Project data is saved",
        "Project data loads after restart",
        "AI response handling works",
        "Invalid input is handled",
        "Empty input is handled",
        "UI navigation works",
        "Project deletion works",
        "Progress persistence works",
        "Report generation works",
    ]

    passed = 0

    for index, test in enumerate(test_cases):

        result = st.checkbox(
            test,
            key=f"test_{index}"
        )

        if result:
            passed += 1

    percentage = int(
        (passed / len(test_cases)) * 100
    )

    st.metric(
        "Testing Score",
        f"{percentage}%"
    )

    st.progress(
        percentage / 100
    )


# ============================================================
# AI MENTOR
# ============================================================

def render_ai_mentor():

    st.markdown(
        '<div class="section-title">🤖 AI Mentor</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project = st.session_state.selected_project

    st.markdown(
        f"### 🧠 Mentor for {get_project_name(project)}"
    )

    st.write(
        "Ask questions about your project, architecture, "
        "technology stack, implementation or documentation."
    )

    if not AI_AVAILABLE:

        st.warning(
            "AI service is currently unavailable. "
            "Check services/ai_mentor.py and the Groq package."
        )

    question = st.chat_input(
        "Ask your AI mentor..."
    )

    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        if AI_AVAILABLE:

            try:

                context = (
                    f"Project: {get_project_name(project)}\n"
                    f"Description: {project.get('description', '')}\n"
                    f"Technologies: {', '.join(project.get('technologies', []))}\n"
                    f"Features: {', '.join(project.get('features', []))}\n"
                )

                prompt = (
                    "You are an AI project mentor helping a student.\n\n"
                    + context
                    + "\n\nStudent question:\n"
                    + question
                )

                answer = ask_mentor(
                    prompt
                )

            except Exception as error:

                answer = (
                    f"AI service error: {error}"
                )

        else:

            answer = (
                "AI Mentor is not connected yet. "
                "Install the Groq package and configure GROQ_API_KEY."
            )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


# ============================================================
# AI CODE ASSISTANT
# ============================================================

def render_code_assistant():

    st.markdown(
        '<div class="section-title">💻 AI Code Assistant</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    code = st.text_area(
        "Paste your code",
        height=300,
        placeholder="Paste Python code here..."
    )

    request = st.text_input(
        "What do you want help with?",
        placeholder="Explain, improve, optimize or fix this code..."
    )

    if st.button(
        "🤖 Analyze Code"
    ):

        if not code.strip():

            st.warning(
                "Please enter some code."
            )

            return

        if AI_AVAILABLE:

            try:

                prompt = f"""
You are a helpful Python AI coding mentor.

Project:
{get_project_name(st.session_state.selected_project)}

User request:
{request}

Code:
{code}

Provide:
1. Explanation
2. Problems found
3. Improvements
4. Corrected code if necessary
"""

                response = ask_mentor(
                    prompt
                )

                st.markdown(
                    "### 🤖 AI Analysis"
                )

                st.write(
                    response
                )

            except Exception as error:

                st.error(
                    f"AI error: {error}"
                )

        else:

            st.warning(
                "AI service is not available."
            )


# ============================================================
# BUG EXPLAINER
# ============================================================

def render_bug_explainer():

    st.markdown(
        '<div class="section-title">🐛 Bug Explainer</div>',
        unsafe_allow_html=True,
    )

    error_message = st.text_area(
        "Paste the error message",
        height=180,
        placeholder="Paste your Python/Streamlit traceback here..."
    )

    code = st.text_area(
        "Optional code",
        height=220,
        placeholder="Paste the related code..."
    )

    if st.button(
        "🔍 Explain Bug"
    ):

        if not error_message.strip():

            st.warning(
                "Please enter an error message."
            )

            return

        if AI_AVAILABLE:

            try:

                prompt = f"""
You are a Python debugging mentor.

Explain this error in beginner-friendly language.

ERROR:
{error_message}

RELATED CODE:
{code}

Provide:
1. What the error means
2. Why it happened
3. Exact fix
4. Corrected code if needed
5. How to avoid it
"""

                response = ask_mentor(
                    prompt
                )

                st.markdown(
                    "### 🧠 Explanation"
                )

                st.write(
                    response
                )

            except Exception as error:

                st.error(
                    f"AI error: {error}"
                )

        else:

            st.warning(
                "AI service is not available."
            )


# ============================================================
# PRESENTATION ASSISTANT
# ============================================================

def render_presentation():

    st.markdown(
        '<div class="section-title">🎤 Presentation Assistant</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project = st.session_state.selected_project

    slides = [
        "Title",
        "Problem Statement",
        "Existing System",
        "Proposed System",
        "Objectives",
        "Technology Stack",
        "System Architecture",
        "Methodology",
        "Implementation",
        "Results",
        "Advantages",
        "Limitations",
        "Future Scope",
        "Conclusion",
    ]

    st.markdown(
        "### 📑 Recommended Slides"
    )

    for i, slide in enumerate(slides, 1):

        st.markdown(
            f"**{i}. {slide}**"
        )

    if st.button(
        "🤖 Generate Presentation Content"
    ):

        if AI_AVAILABLE:

            try:

                prompt = f"""
Create presentation content for this project:

Project:
{get_project_name(project)}

Description:
{project.get('description', '')}

Technologies:
{', '.join(project.get('technologies', []))}

Features:
{', '.join(project.get('features', []))}

Create concise content for:
1. Title
2. Problem Statement
3. Objectives
4. Existing System
5. Proposed System
6. Technology Stack
7. Architecture
8. Methodology
9. Implementation
10. Results
11. Advantages
12. Future Scope
13. Conclusion
"""

                st.session_state.presentation_content = ask_mentor(
                    prompt
                )

            except Exception as error:

                st.error(
                    f"AI error: {error}"
                )

        else:

            st.session_state.presentation_content = (
                "AI service is unavailable. "
                "Configure your Groq integration to generate content."
            )

    if st.session_state.presentation_content:

        st.markdown(
            "### 📄 Generated Content"
        )

        st.write(
            st.session_state.presentation_content
        )


# ============================================================
# PROJECT REPORT
# ============================================================

def render_project_report():

    st.markdown(
        '<div class="section-title">📝 Project Report</div>',
        unsafe_allow_html=True,
    )

    if not current_project_exists():

        st.info(
            "Select a project first."
        )

        return

    project = st.session_state.selected_project

    report = f"""
# {get_project_name(project)}

## 1. Introduction

{project.get("description", "")}

## 2. Problem Statement

{project.get("problem", "")}

## 3. Objectives

The main objectives of this project are:

- Develop an intelligent application.
- Apply suitable AI/ML techniques.
- Provide an easy-to-use interface.
- Store project data reliably.
- Evaluate the developed solution.

## 4. Technologies

{", ".join(project.get("technologies", []))}

## 5. Libraries

{", ".join(project.get("libraries", []))}

## 6. Features

"""

    for feature in project.get(
        "features",
        []
    ):

        report += f"- {feature}\n"

    report += f"""

## 7. Database

{project.get("database", "SQLite")}

## 8. Project Progress

{st.session_state.progress}%

## 9. Conclusion

The project demonstrates how AI and machine learning technologies
can be integrated into a practical software application.

## 10. Future Scope

- Improve AI accuracy.
- Add more datasets.
- Add authentication.
- Improve user interface.
- Add deployment support.
- Add additional AI capabilities.
"""

    st.session_state.generated_report = report

    st.markdown(
        "### 📄 Generated Report"
    )

    st.markdown(
        report
    )

    st.download_button(
        "⬇️ Download Report",
        data=report,
        file_name=(
            get_project_name(project)
            .replace(" ", "_")
            + "_report.md"
        ),
        mime="text/markdown",
    )


# ============================================================
# SETTINGS
# ============================================================

def render_settings():

    st.markdown(
        '<div class="section-title">⚙️ Settings</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 💾 Database"
    )

    st.info(
        f"SQLite currently contains "
        f"{get_project_count()} saved project(s)."
    )

    st.markdown(
        "### 📁 Current Project"
    )

    if current_project_exists():

        st.write(
            get_project_name(
                st.session_state.selected_project
            )
        )

        if st.button(
            "💾 Save Current Project"
        ):

            save_current_project()

            st.success(
                "Project saved."
            )

        if st.button(
            "🗑️ Delete Current Project"
        ):

            name = get_project_name(
                st.session_state.selected_project
            )

            if delete_project(name):

                st.session_state.selected_project = None
                st.session_state.progress = 0
                st.session_state.completed_tasks = []
                st.session_state.tech_stack = []
                st.session_state.database_tables = []
                st.session_state.project_notes = ""

                st.success(
                    "Current project deleted."
                )

                st.rerun()

    else:

        st.info(
            "No project selected."
        )

    st.divider()

    st.markdown(
        "### 🔄 Session"
    )

    if st.button(
        "🧹 Clear AI Chat History"
    ):

        st.session_state.chat_history = []

        st.success(
            "Chat history cleared."
        )


# ============================================================
# NOTES
# ============================================================

def render_notes():

    if not current_project_exists():
        return

    st.markdown(
        "### 📝 Project Notes"
    )

    notes = st.text_area(
        "Notes",
        value=st.session_state.project_notes,
        height=150,
        placeholder="Write project notes here..."
    )

    if notes != st.session_state.project_notes:

        st.session_state.project_notes = notes

        save_current_project()


# ============================================================
# PAGE ROUTER
# ============================================================

page = st.session_state.current_page

if page == "🏠 Home":

    render_home()

elif page == "📊 Dashboard":

    render_dashboard()

elif page == "💡 Project Ideas":

    render_project_ideas()

elif page == "📁 My Projects":

    render_my_projects()

elif page == "🧠 Project Analyzer":

    render_project_analyzer()

elif page == "🗺️ Project Roadmap":

    render_roadmap()

elif page == "🛠️ Technology Stack":

    render_technology_stack()

elif page == "🗄️ Database Designer":

    render_database_designer()

elif page == "📚 Resources":

    render_resources()

elif page == "📈 Progress Tracker":

    render_progress_tracker()

elif page == "🧪 Testing Assistant":

    render_testing_assistant()

elif page == "🤖 AI Mentor":

    render_ai_mentor()

elif page == "💻 AI Code Assistant":

    render_code_assistant()

elif page == "🐛 Bug Explainer":

    render_bug_explainer()

elif page == "🎤 Presentation Assistant":

    render_presentation()

elif page == "📝 Project Report":

    render_project_report()

elif page == "⚙️ Settings":

    render_settings()


# ============================================================
# GLOBAL PROJECT NOTES
# ============================================================

if (
    current_project_exists()
    and page in [
        "📁 My Projects",
        "📊 Dashboard",
        "🧠 Project Analyzer",
        "🗺️ Project Roadmap",
        "🛠️ Technology Stack",
        "🗄️ Database Designer",
        "📈 Progress Tracker",
    ]
):

    with st.expander(
        "📝 Project Notes"
    ):

        notes = st.text_area(
            "Add notes about your project",
            value=st.session_state.project_notes,
            key="global_project_notes",
        )

        if st.button(
            "💾 Save Notes"
        ):

            st.session_state.project_notes = notes

            save_current_project()

            st.success(
                "Notes saved to SQLite."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br><br>
    <div style="
        text-align:center;
        padding:25px;
        color:#64748b;
    ">
        <b>🤖 AI Project Mentor</b>
        <br>
        Turn Your Ideas Into Intelligent Projects.
        <br>
        <small>
            Built with Python • Streamlit • SQLite • AI
        </small>
    </div>
    """,
    unsafe_allow_html=True,
)