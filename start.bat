@echo off
echo ========================================
echo   AI Insight & Lingua Dashboard
echo   正在启动应用...
echo ========================================
echo.

cd /d "%~dp0"
streamlit run app.py --server.port 8501 --server.headless true

pause

