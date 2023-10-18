@echo off

rem Change directory to the streamlit_app folder
cd /d ".\streamlit_app"

rem Run the Streamlit App
start "Streamlit App" streamlit run app.py

rem Change directory to the backend folder
cd /d "..\..\backend"

rem Run the Python Main
start "Python Main" python main.py
