@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Setup complete! Run the following commands:
echo venv\Scripts\activate
echo python src/web/app.py
