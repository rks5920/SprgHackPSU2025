# SprgHackPSU2025

Description here

## Backend Setup

1. Enter the backend folder: `cd backend`
2. Start the virtual environment: `source .venv/bin/activate`
3. Start the server: `python3 bone_server.py`
4. Play an audio (replace 1 with your targeted button): `curl http://104.39.94.143:5000/1`
5. Edit an audio (replace 1 with your targeted button): `curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"hello world\"}" http://104.39.94.143:5000/1/edit`

*Note: you must be on psu wifi to send requests

