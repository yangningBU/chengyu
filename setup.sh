#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Setup complete! Virtual environment is activated."
echo "To activate the virtual environment in the future, run: source venv/bin/activate" 