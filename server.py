from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from algorithms.caesar import CaesarCipherTR
from algorithms.vigenere import VigenereCipherTR
from algorithms.affine import AffineCipherTR
from algorithms.railfence import RailFenceCipherTR
from algorithms.route import RouteCipherTR
from algorithms.columnar import ColumnarCipherTR
from algorithms.polybius import PolybiusCipherTR
from algorithms.hill import HillCipherTR
import uvicorn
import traceback
import ast  
import numpy as np



app = FastAPI()

class CryptoRequest(BaseModel):
    algorithm: str
    operation: str  
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
            "Affine": AffineCipherTR(),
            "Rail Fence": RailFenceCipherTR(),
            "Route": RouteCipherTR(), 
            "Columnar": ColumnarCipherTR(),
            "Polybius": PolybiusCipherTR(),
            "Hill": HillCipherTR(),
        }

    

    def _parse_hill_matrix(self, key_str):
        key_str = key_str.strip()
        if key_str.startswith("[") and key_str.endswith("]"):
            try:
                matrix_list = ast.literal_eval(key_str)
            except:
                raise HTTPException(status_code=400, detail="Hatalı Hill matrisi formatı. Örn: [[3,3],[2,5]]")
        else:
            rows = [r for r in key_str.replace(';','\n').split('\n') if r.strip()]
            matrix_list = []
            for row in rows:
                nums = [int(x) for x in row.replace(',', ' ').split()]
                matrix_list.append(nums)
        
        matrix = np.array(matrix_list)
        if matrix.shape[0] != matrix.shape[1]:
            raise HTTPException(status_code=400, detail="Hill matrisi kare olmalı (2x2 veya 3x3)")
        return matrix



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
        elif algorithm == "Rail Fence":
            if key1 is not None:
                self.algorithms[algorithm].rails = int(key1)
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Route":
            if key1 is not None:
                self.algorithms[algorithm].cols = int(key1)
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Columnar":
            if key1 is not None:
                self.algorithms[algorithm].key = str(key1)
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Polybius":
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Hill":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="Hill anahtar matrisi boş olamaz")
            matrix = self._parse_hill_matrix(key1)
            self.algorithms[algorithm].key_matrix = matrix
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
        elif algorithm == "Rail Fence":
            if key1 is not None:
                self.algorithms[algorithm].rails = int(key1)
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Route":
            if key1 is not None:
                self.algorithms[algorithm].cols = int(key1)
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Columnar":
            if key1 is not None:
                self.algorithms[algorithm].key = str(key1)
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Polybius":
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Hill":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="Hill anahtar matrisi boş olamaz")
            matrix = self._parse_hill_matrix(key1)
            self.algorithms[algorithm].key_matrix = matrix
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

