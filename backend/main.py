from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai
from services.file_service import FileService
from services.gemini_service import GeminiService
import logging

# Pydantic models for request bodies
class ImageAnalysisRequest(BaseModel):
    imageUrl: str
    prompt: str = None

class ConversationAnalysisRequest(BaseModel):
    transcript: str = None
    audioUrl: str = None

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Plivo AI Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini with new client API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Set environment variable for the new genai client
os.environ["GOOGLE_API_KEY"] = gemini_api_key

# Initialize services
file_service = FileService()
gemini_service = GeminiService()

@app.get("/")
async def root():
    return {"message": "Plivo Backend is running with Python & Gemini!"}

@app.post("/api/v1/summarize")
async def summarize_content(
    inputType: str = Form(...),
    url: str = Form(None),
    text: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        logger.info(f"Received summarization request: inputType={inputType}")
        
        extracted_text = ""
        
        if inputType == "URL":
            if not url:
                raise HTTPException(status_code=400, detail="URL is required for URL input type")
            logger.info(f"Processing URL: {url}")
            extracted_text = await file_service.extract_text_from_url(url)
            
        elif inputType == "Text":
            if not text:
                raise HTTPException(status_code=400, detail="Text is required for Text input type")
            logger.info(f"Processing text input: {text[:100]}...")
            extracted_text = text
            
        elif inputType == "File":
            if not file:
                raise HTTPException(status_code=400, detail="File is required for File input type")
            logger.info(f"Processing file: {file.filename}")
            extracted_text = await file_service.extract_text_from_file(file)
            
        else:
            raise HTTPException(status_code=400, detail="Invalid input type")
        
        if not extracted_text or not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the source")
        
        logger.info(f"Extracted text length: {len(extracted_text)}")
        
        # Generate summary using Gemini
        logger.info("Calling Gemini service for summarization")
        summary = await gemini_service.summarize_text(extracted_text)
        logger.info("Summarization completed successfully")
        
        return {"summary": summary}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in summarization: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to summarize content: {str(e)}")

@app.post("/api/v1/analyze-image")
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form(None)
):
    try:
        logger.info(f"Received image analysis request: filename={image.filename}")
        
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        analysis_prompt = prompt or "Analyze this image and describe what you see in detail."
        logger.info(f"Using prompt: {analysis_prompt}")
        
        # Analyze image using Gemini File API
        analysis = await gemini_service.analyze_image_from_file(image, analysis_prompt)
        
        return {"analysis": analysis}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")

@app.post("/api/v1/analyze-conversation")
async def analyze_conversation(
    audio: UploadFile = File(...)
):
    try:
        logger.info(f"Received conversation analysis request: filename={audio.filename}")
        
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Process audio file through speech-to-text, diarization, and analysis
        analysis_result = await gemini_service.analyze_conversation_from_audio(audio)
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in conversation analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze conversation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5001))
    uvicorn.run(app, host="0.0.0.0", port=port)
