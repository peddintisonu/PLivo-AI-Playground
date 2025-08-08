@echo off
echo 🚀 Setting up Plivo AI Playground...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+ first.
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js are installed

:: Setup Backend
echo 📦 Setting up backend...
cd backend

:: Create virtual environment
python -m venv .venv

:: Activate virtual environment (Windows)
call .venv\Scripts\activate.bat

:: Install Python dependencies
pip install -r requirements.txt

:: Copy environment file
if not exist .env (
    copy .env.example .env
    echo ⚠️ Please edit backend\.env and add your API keys!
)

echo ✅ Backend setup complete

:: Setup Frontend
echo 📦 Setting up frontend...
cd ..\frontend

:: Install Node dependencies
npm install

:: Copy environment file
if not exist .env (
    copy .env.example .env
    echo ℹ️ Frontend environment file created with default values
)

echo ✅ Frontend setup complete

cd ..

echo.
echo 🎉 Setup complete! Next steps:
echo.
echo 1. Add your Gemini API key to backend\.env
echo 2. Start the backend: cd backend ^&^& python main.py
echo 3. Start the frontend: cd frontend ^&^& npm run dev
echo 4. Open http://localhost:5173 in your browser
echo.
echo 📚 See README.md for detailed instructions
pause
