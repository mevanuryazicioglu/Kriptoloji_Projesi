# Cryptology Project
This project enables data transfer from client to server. The client sends user input through a GUI, and the server receives the message, encrypts/decrypts it and responds.

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- Requests

## Installation

### Clone project
```bash
git clone https://github.com/mevanuryazicioglu/Kriptoloji_Projesi/
cd Kriptoloji_Projesi
```

### Install dependencies
```bash
pip install -r requirements.txt
```
Or install manually:
```bash
pip install fastapi uvicorn requests pydantic
```

## How to Run

This project uses a client-server architecture. You need to run both the server and client:

### 1. Start the Server
Open a terminal and run:
```bash
python3 server.py
```
The server will start on `http://127.0.0.1:8000`

### 2. Start the Client (GUI)
Open another terminal and run:
```bash
python3 client.py
```
