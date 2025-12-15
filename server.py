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
from algorithms.des import DESCipherTR
from algorithms.des_k import DESCipherTR as DESLibraryCipherTR # Kütüphaneli DES importu
from algorithms.aes import AESCipherTR
from algorithms.aes_k import AESCipherTR as AESLibraryCipherTR
from algorithms.rsa import RSACipherTR
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
    rsa_public_key: Optional[dict] = None
    rsa_private_key: Optional[dict] = None

class CryptoResponse(BaseModel):
    result: str
    algorithm: str
    operation: str
    public_key: Optional[dict] = None
    private_key: Optional[dict] = None

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
            "DES": None,
            "AES": None,
            "AES Kütüphaneli": None,
            "RSA": None,
            "DES Kütüphaneli": None,
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
        elif algorithm == "DES":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="DES anahtarı boş olamaz")
            self.algorithms["DES"] = DESCipherTR(key1)
            return self.algorithms["DES"].encrypt(text)
        elif algorithm == "AES":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="AES anahtarı boş olamaz")
            if len(key1) not in [16, 24, 32]:
                raise HTTPException(status_code=400, detail="AES anahtarı 16, 24 veya 32 karakter olmalı")
            
            self.algorithms["AES"] = AESCipherTR(key1)
            return self.algorithms["AES"].encrypt(text)
        elif algorithm == "AES Kütüphaneli":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="AES Kütüphaneli anahtarı boş olamaz")
            if len(key1) not in [16, 24, 32]:
                raise HTTPException(status_code=400, detail="AES Kütüphaneli anahtarı 16, 24 veya 32 karakter olmalı")
            
            aes_lib_cipher = AESLibraryCipherTR(key1)
            return aes_lib_cipher.encrypt(text)
        elif algorithm == "DES Kütüphaneli":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="DES Kütüphaneli anahtarı boş olamaz")
            if len(key1) != 8:
                raise HTTPException(status_code=400, detail="DES Kütüphaneli anahtarı 8 karakter olmalı")
            
            des_lib_cipher = DESLibraryCipherTR(key1)
            return des_lib_cipher.encrypt(text)
        elif algorithm == "RSA":
            public_key = key1 if isinstance(key1, dict) and "e" in key1 and "n" in key1 else None
            
            if public_key:
                rsa_cipher = RSACipherTR.from_keys(public_key)
                cipher_text = rsa_cipher.encrypt(text)
                return {"cipher": cipher_text, "public": public_key, "private": None} # Özel anahtarı geri döndürmüyoruz
            else:
                rsa_cipher = RSACipherTR()
                cipher_text = rsa_cipher.encrypt(text)
                return {
                    "cipher": cipher_text,
                    "public": rsa_cipher.export_public(),
                    "private": rsa_cipher.export_private()
                }






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
            self.algorithms[algorithm] = HillCipherTR()   
            self.algorithms[algorithm].key_matrix = matrix
            return self.algorithms[algorithm].decrypt(text)

        elif algorithm == "DES":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="DES anahtarı boş olamaz")
            self.algorithms["DES"] = DESCipherTR(key1)
            return self.algorithms["DES"].decrypt(text)
        elif algorithm == "AES":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="AES anahtarı boş olamaz")
            if len(key1) not in [16, 24, 32]:
                raise HTTPException(status_code=400, detail="AES anahtarı 16, 24 veya 32 karakter olmalı")
            
            self.algorithms["AES"] = AESCipherTR(key1)
            return self.algorithms["AES"].decrypt(text)
        elif algorithm == "AES Kütüphaneli":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="AES Kütüphaneli anahtarı boş olamaz")
            if len(key1) not in [16, 24, 32]:
                raise HTTPException(status_code=400, detail="AES Kütüphaneli anahtarı 16, 24 veya 32 karakter olmalı")
            
            aes_lib_cipher = AESLibraryCipherTR(key1)
            return aes_lib_cipher.decrypt(text)
        elif algorithm == "DES Kütüphaneli":
            if key1 is None or key1.strip() == "":
                raise HTTPException(status_code=400, detail="DES Kütüphaneli anahtarı boş olamaz")
            if len(key1) != 8:
                raise HTTPException(status_code=400, detail="DES Kütüphaneli anahtarı 8 karakter olmalı")
            
            des_lib_cipher = DESLibraryCipherTR(key1)
            return des_lib_cipher.decrypt(text)
        elif algorithm == "RSA":
            if key1 is None:
                raise HTTPException(status_code=400, detail="RSA decrypt için private key (key1) gerekli")
            
            private_key_components = key1 # key1 artık doğrudan private_key_components olarak düşünülüyor

            try:
                rsa_cipher = RSACipherTR.from_keys(private_key_components)
                return rsa_cipher.decrypt(text)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"RSA private key formatı hatalı veya deşifreleme başarısız: {e}")




        






server = Server()

@app.post("/crypto", response_model=CryptoResponse)
async def process_crypto(request: CryptoRequest):
    try:
        if request.operation == "encrypt":
            if request.algorithm == "RSA":
                result = server.encrypt(request.algorithm, request.text, request.rsa_public_key)
            else:
                result = server.encrypt(request.algorithm, request.text, request.key1, request.key2)
        elif request.operation == "decrypt":
            if request.algorithm == "RSA":
                result = server.decrypt(request.algorithm, request.text, request.rsa_private_key)
            else:
                result = server.decrypt(request.algorithm, request.text, request.key1, request.key2)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation. Use 'encrypt' or 'decrypt'")

        if result is None:
            raise HTTPException(status_code=400, detail="Encryption/Decryption failed")

        # Eğer RSA encrypt dict döndürdüyse burayı ayarla:
        if isinstance(result, dict) and request.algorithm == "RSA" and request.operation == "encrypt":
            return CryptoResponse(
                result=result["cipher"],
                algorithm=request.algorithm,
                operation=request.operation,
                public_key=result.get("public"),
                private_key=result.get("private")
            )

        # Normal (string) durum
        return CryptoResponse(
            result=str(result),
            algorithm=request.algorithm,
            operation=request.operation
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

