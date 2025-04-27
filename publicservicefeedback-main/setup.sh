#!/bin/bash
echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete! Run the following commands:"
echo "source venv/bin/activate"
echo "python src/web/app.py"
