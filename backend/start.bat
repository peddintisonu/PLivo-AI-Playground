@echo off

echo Installing Python dependencies...
pip install -r requirements.txt

echo Starting FastAPI server...
python -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
