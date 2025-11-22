#!/bin/bash
# setup.sh

echo "Setting up Transcription App..."

# Backend setup
cd ../backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
echo "Please edit backend/.env with your configuration"

# Create database
python manage.py migrate

# Frontend setup
cd ../frontend
npm install
cp .env.example .env
echo "Please edit frontend/.env with your configuration"

echo "Setup complete! Don't forget to start Redis and MySQL."