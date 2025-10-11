from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from algorithms.caesar import CaesarCipherTR
from algorithms.vigenere import VigenereCipherTR
from algorithms.affine import AffineCipherTR
import uvicorn
import traceback

app = FastAPI()

class CryptoRequest(BaseModel):
    algorithm: str
    operation: str  # "encrypt" or "decrypt"
    text: str
    key1: Any = None
    key2: Optional[int] = None

class CryptoResponse(BaseModel):
    result: str
    algorithm: str
    operation: str

class Server:
    def __init__(self):
        self.algorithms = {
            "Caesar": CaesarCipherTR(),
            "Vigenere": VigenereCipherTR(),
            "Affine": AffineCipherTR()
        }

    def encrypt(self, algorithm, text, key1=None, key2=None):
        if algorithm == "Caesar":
            if key1 is not None:
                self.algorithms[algorithm].shift = key1
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Vigenere":
            if key1 is not None:
                self.algorithms[algorithm].key = key1
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Affine":
            if key1 is not None and key2 is not None:
                self.algorithms[algorithm].a = key1
                self.algorithms[algorithm].b = key2
            return self.algorithms[algorithm].encrypt(text)

    def decrypt(self, algorithm, text, key1=None, key2=None):
        if algorithm == "Caesar":
            if key1 is not None:
                self.algorithms[algorithm].shift = key1
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Vigenere":
            if key1 is not None:
                self.algorithms[algorithm].key = key1
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Affine":
            if key1 is not None and key2 is not None:
                self.algorithms[algorithm].a = key1
                self.algorithms[algorithm].b = key2
            return self.algorithms[algorithm].decrypt(text)

server = Server()

@app.post("/crypto", response_model=CryptoResponse)
async def process_crypto(request: CryptoRequest):
    try:
        if request.operation == "encrypt":
            result = server.encrypt(request.algorithm, request.text, request.key1, request.key2)
        elif request.operation == "decrypt":
            result = server.decrypt(request.algorithm, request.text, request.key1, request.key2)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation. Use 'encrypt' or 'decrypt'")
        
        if result is None:
            raise HTTPException(status_code=400, detail="Encryption/Decryption failed")
        
        return CryptoResponse(
            result=result,
            algorithm=request.algorithm,
            operation=request.operation
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e)) from e

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
