from fastapi import UploadFile, HTTPException
import requests
import PyPDF2
from docx import Document
import io
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FileService:
    
    async def extract_text_from_url(self, url: str) -> str:
        """Extract text content from a URL"""
        try:
            logger.info(f"Fetching content from URL: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # For now, return the raw text content
            # You could add HTML parsing here if needed
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Error fetching URL content: {str(e)}")
            raise Exception(f"Failed to fetch content from URL: {str(e)}")
    
    async def extract_text_from_file(self, file: UploadFile) -> str:
        """Extract text from uploaded file based on file type"""
        try:
            logger.info(f"Processing file: {file.filename}, type: {file.content_type}")
            
            # Read file content
            file_content = await file.read()
            
            if file.content_type == "application/pdf":
                return await self._extract_text_from_pdf(file_content)
            elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return await self._extract_text_from_docx(file_content)
            elif file.content_type and file.content_type.startswith("text/"):
                return file_content.decode("utf-8")
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Unsupported file type. Please upload PDF, DOCX, or text files."
                )
                
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            logger.error(f"Error processing file: {str(e)}")
            raise Exception(f"Failed to process file: {str(e)}")
    
    async def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if not text.strip():
                raise Exception("No extractable text found in PDF")
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    async def _extract_text_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            if not text.strip():
                raise Exception("No text found in DOCX file")
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
