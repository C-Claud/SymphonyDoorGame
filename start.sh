#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed. Starting server..."
python app.py &
sleep 3
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://127.0.0.1:5000
else
    xdg-open http://127.0.0.1:5000
fi
echo "Server is running! Press Ctrl+C to exit."
wait