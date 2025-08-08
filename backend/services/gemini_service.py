from google import genai
import requests
import tempfile
import os
from typing import Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = genai.Client()
    
    async def summarize_text(self, text: str) -> str:
        """Summarize text using Gemini"""
        try:
            prompt = f"""
            Please provide a concise and informative summary of the following text. 
            Focus on the main points and key insights:
            
            {text}
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt]
            )
            return response.text
            
        except Exception as e:
            logger.error(f"Error in text summarization: {str(e)}")
            raise Exception(f"Failed to summarize text: {str(e)}")
    
    async def analyze_image_from_url(self, image_url: str, prompt: str) -> str:
        """Analyze image from URL using Gemini File API"""
        try:
            logger.info(f"Downloading image from URL: {image_url}")
            
            # Download the image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Determine the file extension
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                extension = '.jpg'
            elif 'png' in content_type:
                extension = '.png'
            elif 'webp' in content_type:
                extension = '.webp'
            elif 'gif' in content_type:
                extension = '.gif'
            else:
                extension = '.jpg'  # Default fallback
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name
            
            try:
                logger.info(f"Uploading image to Gemini File API")
                
                # Upload to Gemini File API
                uploaded_file = self.client.files.upload(file=Path(tmp_file_path))
                logger.info(f"File uploaded successfully: {uploaded_file.name}")
                
                # Wait for processing
                import time
                while uploaded_file.state.name == "PROCESSING":
                    logger.info("File is still processing...")
                    time.sleep(2)
                    uploaded_file = self.client.files.get(uploaded_file.name)
                
                if uploaded_file.state.name != "ACTIVE":
                    raise Exception(f"File processing failed: {uploaded_file.state.name}")
                
                logger.info("File processed successfully, analyzing image...")
                
                # Analyze the image
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[uploaded_file, prompt]
                )
                
                # Clean up the uploaded file
                self.client.files.delete(name=uploaded_file.name)
                logger.info("Image file deleted from Gemini")
                
                return response.text
                
            finally:
                # Always clean up local file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    logger.info("Local temporary file deleted")
                    
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            raise Exception(f"Failed to download image from URL: {str(e)}")
        except Exception as e:
            logger.error(f"Error in image analysis: {str(e)}")
            raise Exception(f"Failed to analyze image: {str(e)}")
    
    async def analyze_conversation(self, conversation_text: str) -> str:
        """Analyze conversation text using Gemini"""
        try:
            prompt = f"""
            Please analyze this conversation and provide insights including:
            1. Summary of the conversation
            2. Key topics discussed
            3. Main points from each participant
            4. Any action items or decisions made
            
            Conversation:
            {conversation_text}
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt]
            )
            return response.text
            
        except Exception as e:
            logger.error(f"Error in conversation analysis: {str(e)}")
            raise Exception(f"Failed to analyze conversation: {str(e)}")
    
    async def summarize_pdf_file(self, pdf_path: str) -> str:
        """Summarize PDF file using Gemini File API"""
        try:
            logger.info(f"Uploading PDF to Gemini File API: {pdf_path}")
            
            # Upload PDF file to Gemini
            uploaded_file = self.client.files.upload(file=Path(pdf_path))
            logger.info(f"PDF uploaded successfully: {uploaded_file.name}")
            
            # Generate summary
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["Give me a comprehensive summary of this PDF file.", uploaded_file]
            )
            
            # Clean up the uploaded file
            self.client.files.delete(name=uploaded_file.name)
            logger.info("PDF file deleted from Gemini")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in PDF summarization: {str(e)}")
            raise Exception(f"Failed to summarize PDF: {str(e)}")
    
    async def analyze_audio_file(self, audio_path: str, prompt: str = "Describe this audio clip") -> str:
        """Analyze audio file using Gemini File API"""
        try:
            logger.info(f"Uploading audio to Gemini File API: {audio_path}")
            
            # Upload audio file to Gemini
            uploaded_file = self.client.files.upload(file=Path(audio_path))
            logger.info(f"Audio uploaded successfully: {uploaded_file.name}")
            
            # Analyze the audio
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[uploaded_file, prompt]
            )
            
            # Clean up the uploaded file
            self.client.files.delete(name=uploaded_file.name)
            logger.info("Audio file deleted from Gemini")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in audio analysis: {str(e)}")
            raise Exception(f"Failed to analyze audio: {str(e)}")
    
    async def analyze_image_from_file(self, image_file, prompt: str) -> str:
        """Analyze image from uploaded file using Gemini File API"""
        try:
            logger.info(f"Processing uploaded image: {image_file.filename}")
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{image_file.filename}") as tmp_file:
                content = await image_file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            logger.info("Uploading image to Gemini File API")
            
            # Upload image to Gemini File API
            uploaded_file = self.client.files.upload(file=Path(tmp_file_path))
            logger.info(f"File uploaded successfully: {uploaded_file.name}")
            
            # Wait for processing
            import time
            while uploaded_file.state.name == "PROCESSING":
                logger.info("File is still processing...")
                time.sleep(2)
                uploaded_file = self.client.files.get(uploaded_file.name)
            
            if uploaded_file.state.name != "ACTIVE":
                raise Exception(f"File processing failed: {uploaded_file.state.name}")
            
            logger.info("File processed successfully, analyzing image...")
            
            # Analyze the image
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[uploaded_file, prompt]
            )
            
            # Clean up files
            self.client.files.delete(name=uploaded_file.name)
            os.unlink(tmp_file_path)
            logger.info("Local temporary file deleted")
            
            return response.text
            
        except Exception as e:
            # Clean up on error
            if 'tmp_file_path' in locals():
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
            logger.error(f"Error in image analysis: {str(e)}")
            raise Exception(f"Failed to analyze image: {str(e)}")
    
    async def analyze_conversation_from_audio(self, audio_file) -> dict:
        """Process audio file for conversation analysis: STT + Diarization + Summary"""
        try:
            logger.info(f"Processing audio file for conversation analysis: {audio_file.filename}")
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{audio_file.filename}") as tmp_file:
                content = await audio_file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            logger.info("Uploading audio to Gemini File API for transcription")
            
            # Upload audio to Gemini File API
            uploaded_file = self.client.files.upload(file=Path(tmp_file_path))
            logger.info(f"Audio uploaded successfully: {uploaded_file.name}")
            
            # Wait for processing
            import time
            while uploaded_file.state.name == "PROCESSING":
                logger.info("Audio is still processing...")
                time.sleep(2)
                uploaded_file = self.client.files.get(uploaded_file.name)
            
            if uploaded_file.state.name != "ACTIVE":
                raise Exception(f"Audio processing failed: {uploaded_file.state.name}")
            
            logger.info("Audio processed successfully, generating transcript...")
            
            # Step 1: Generate transcript
            transcript_prompt = """
            Please transcribe this audio file. Provide a clean, accurate transcription of all speech content.
            """
            transcript_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[uploaded_file, transcript_prompt]
            )
            transcript = transcript_response.text
            
            # Step 2: Generate diarized transcript (manual diarization)
            diarization_prompt = f"""
            Based on this transcript: "{transcript}"
            
            Please provide a speaker-diarized version assuming up to 2 speakers (Speaker 1 and Speaker 2).
            Analyze voice changes, conversation patterns, and context to identify when different speakers are talking.
            Format the output as:
            
            Speaker 1: [text]
            Speaker 2: [text]
            Speaker 1: [text]
            etc.
            
            If you can only detect one speaker, label everything as "Speaker 1".
            """
            
            diarized_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[diarization_prompt]
            )
            diarized_transcript = diarized_response.text
            
            # Step 3: Generate summary and analysis
            summary_prompt = f"""
            Based on this conversation transcript: "{transcript}"
            
            Please provide:
            1. A concise summary of the conversation
            2. Key topics discussed
            3. Main points from each speaker
            4. Any action items or decisions made
            """
            
            summary_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[summary_prompt]
            )
            summary = summary_response.text
            
            # Clean up files
            self.client.files.delete(name=uploaded_file.name)
            os.unlink(tmp_file_path)
            logger.info("Audio file cleanup completed")
            
            return {
                "transcript": transcript,
                "diarization": diarized_transcript,
                "summary": summary
            }
            
        except Exception as e:
            # Clean up on error
            if 'tmp_file_path' in locals():
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
            logger.error(f"Error in conversation analysis: {str(e)}")
            raise Exception(f"Failed to analyze conversation: {str(e)}")
