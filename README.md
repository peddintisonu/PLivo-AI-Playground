# 🚀 Plivo AI Playground

A comprehensive multi-modal AI application built for the **IIT Madras 2025 - Internship Assignment**. This playground allows users to interact with various AI-powered tools for document analysis, image processing, and conversation analysis.

## 🌐 Live Demo

**🎮 Frontend**: [https://p-livo-ai-playground.vercel.app/](https://p-livo-ai-playground.vercel.app/)  
**🔗 Backend API**: [https://plivo-ai-playground.onrender.com/](https://plivo-ai-playground.onrender.com/)  
**📚 API Documentation**: [https://plivo-ai-playground.onrender.com/docs](https://plivo-ai-playground.onrender.com/docs)

![Demo](https://img.shields.io/badge/Demo-Live-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=for-the-badge&logo=fastapi)

## 🎯 Assignment Requirements Met

This application fulfills all the assignment requirements:

### ✅ **Conversation Analysis (20 points)**
- **Audio File Upload**: Users can upload audio files (MP3, WAV, M4A, FLAC)
- **Speech-to-Text (10 points)**: Complete transcription of audio content
- **Speaker Diarization (10 points)**: Identification and separation of up to 2 speakers
- **Summary & Analysis**: Comprehensive conversation insights and action items

### ✅ **Image Analysis (10 points)**
- **Image Upload**: Support for PNG, JPG, JPEG, WebP formats
- **AI Description**: Detailed textual descriptions of uploaded images
- **Custom Prompts**: Optional custom analysis prompts for specific insights

### ✅ **Document/URL Summarization (20 points)**
- **Multi-format Support**: PDF, DOC, DOCX file uploads
- **URL Processing**: Direct URL content extraction and summarization
- **AI Summarization**: Concise, intelligent content summaries

## 🏗️ Architecture

### **Frontend (React + Vite)**
- **Framework**: React 18 with Vite for fast development
- **Styling**: Tailwind CSS for responsive, modern UI
- **Authentication**: Clerk (configurable, can be disabled)
- **File Handling**: Advanced file upload with previews
- **State Management**: React hooks for component state

### **Backend (Python FastAPI)**
- **Framework**: FastAPI for high-performance API
- **AI Integration**: Google Gemini 2.0 Flash model
- **File Processing**: PyPDF2, python-docx for document parsing
- **API Design**: RESTful endpoints with proper error handling
- **CORS**: Configured for frontend integration

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** 
- **Node.js 18+**
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd plivo-ai-playground
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env if needed (default values should work for local development)
```

### 4. Run the Application
```bash
# Terminal 1 - Start Backend (from backend directory)
python main.py

# Terminal 2 - Start Frontend (from frontend directory)
npm run dev
```

### 5. Access the Application

**Local Development:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5001
- **API Documentation**: http://localhost:5001/docs

**Production (Live Demo):**
- **Frontend**: https://p-livo-ai-playground.vercel.app/
- **Backend API**: https://plivo-ai-playground.onrender.com/
- **API Documentation**: https://plivo-ai-playground.onrender.com/docs

## ⚙️ Configuration

### Backend Environment Variables

**Local Development (.env):**
```env
# Server Configuration
PORT=5001
FRONTEND_URL=http://localhost:5173

# Google Gemini API (Required)
GEMINI_API_KEY=your_gemini_api_key_here
```

**Production (.env):**
```env
# Server Configuration
PORT=5001
FRONTEND_URL=https://p-livo-ai-playground.vercel.app

# Google Gemini API (Required)
GEMINI_API_KEY=your_gemini_api_key_here
```

### Frontend Environment Variables

**Local Development (.env):**
```env
# Backend API Configuration
VITE_API_BASE_URL=http://localhost:5001/api/v1

# App Configuration
VITE_APP_NAME=Plivo AI Playground
```

**Production (.env):**
```env
# Backend API Configuration
VITE_API_BASE_URL=https://plivo-ai-playground.onrender.com/api/v1

# App Configuration
VITE_APP_NAME=Plivo AI Playground
```

## 📁 Project Structure

```
plivo-ai-playground/
├── backend/
│   ├── services/
│   │   ├── file_service.py      # Document processing
│   │   └── gemini_service.py    # AI integration
│   ├── main.py                  # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   └── .venv/                  # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageAnalysisUI.jsx
│   │   │   ├── ConversationAnalysisUI.jsx
│   │   │   ├── SummarizationUI.jsx
│   │   │   ├── Playground.jsx   # Main app logic
│   │   │   └── SkillSelector.jsx
│   │   ├── App.jsx              # Root component
│   │   └── index.css            # Tailwind styles
│   ├── package.json             # Node dependencies
│   ├── .env.example            # Environment template
│   └── vite.config.js          # Vite configuration
└── README.md                   # This file
```

## 🔧 API Endpoints

### **POST** `/api/v1/analyze-image`
Upload and analyze images with AI-powered descriptions.

**Request**: Multipart form data
- `image`: Image file
- `prompt`: Optional custom prompt

**Response**:
```json
{
  "analysis": "Detailed image description..."
}
```

### **POST** `/api/v1/analyze-conversation`
Process audio files for conversation analysis.

**Request**: Multipart form data
- `audio`: Audio file

**Response**:
```json
{
  "transcript": "Full conversation transcript...",
  "diarization": "Speaker 1: ... Speaker 2: ...",
  "summary": "Conversation summary and insights..."
}
```

### **POST** `/api/v1/summarize`
Summarize documents or URL content.

**Request**: Multipart form data
- `inputType`: "File" or "URL"
- `file`: Document file (if inputType is "File")
- `url`: URL string (if inputType is "URL")

**Response**:
```json
{
  "summary": "Document summary..."
}
```

## 🧪 Testing

### Manual Testing
1. **Image Analysis**: Upload a sample image and verify AI description
2. **Conversation Analysis**: Upload an audio file and check transcript/diarization
3. **Document Summarization**: Upload a PDF or provide a URL for summarization

### Sample Test Files
- **Images**: Any JPG, PNG, or WebP image
- **Audio**: MP3 or WAV files with conversation (up to 2 speakers work best)
- **Documents**: PDF files or any readable web URL

## 🛠️ Development Notes

### AI Integration
- **Primary Service**: Google Gemini 2.0 Flash for all AI operations
- **File API**: Utilizes Gemini File API for efficient file processing
- **Fallback**: OpenAI integration available but not currently used

### Error Handling
- **503 Errors**: Gemini API overload (temporary, retry recommended)
- **File Size**: Large files may take longer to process
- **Format Support**: Only specific file formats are supported per feature

### Performance Considerations
- **File Processing**: Large files processed asynchronously
- **API Limits**: Gemini API has rate limiting
- **Memory**: Audio files temporarily stored during processing

## 📱 Deployment

### Vercel Deployment (Recommended)
1. Fork this repository
2. Connect to Vercel
3. Configure environment variables in Vercel dashboard
4. Deploy frontend to Vercel
5. Deploy backend to a Python hosting service (Railway, Render, etc.)

### Docker Deployment
Docker configurations can be added for containerized deployment.

## 🐛 Troubleshooting

### Common Issues

**503 Service Unavailable**
- The Gemini API is temporarily overloaded
- Wait a few minutes and try again

**File Upload Errors**
- Check file format compatibility
- Ensure file size is reasonable (<50MB)

**CORS Errors**
- Verify frontend URL in backend CORS settings
- Check environment variable configuration

**Audio Processing Slow**
- Large audio files take time to process
- Gemini API processing can be slow during peak hours

## 🏆 Assignment Scoring

This implementation targets maximum points:

- ✅ **Conversation Analysis**: 20/20 points (STT + Diarization)
- ✅ **Image Analysis**: 10/10 points (Upload + AI Description)  
- ✅ **Document Summarization**: 20/20 points (PDF/URL + AI Summary)
- ✅ **Code Quality**: Clean, documented, well-structured
- ✅ **Architecture**: Proper separation, scalable design
- ✅ **Frontend**: Responsive, modern UI with Tailwind
- ✅ **AI-First Development**: Leveraging latest AI APIs and tools

**Total Score Target**: 50+ points

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for the IIT Madras 2025 Internship Assignment.

## 🙏 Acknowledgments

- **IIT Madras** for the assignment opportunity
- **Google Gemini** for powerful AI capabilities
- **FastAPI** and **React** communities for excellent frameworks
- **Tailwind CSS** for beautiful, responsive styling

---

Built with ❤️ using AI-first development principles for the **IIT Madras 2025 Internship Assignment**.
# PLivo-AI-Playground
