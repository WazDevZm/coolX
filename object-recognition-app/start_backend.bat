@echo off
echo Starting Object Detection Backend...
echo.

cd python_backend
echo Installing Python dependencies...
python setup.py

echo.
echo Starting Python backend server...
python server.py

pause
