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
from algorithms.des_k import DESCipherTR as DESLibraryCipherTR
from algorithms.aes import AESCipherTR
from algorithms.aes_k import AESCipherTR as AESLibraryCipherTR

import uvicorn
import traceback
import ast
import numpy as np

app = FastAPI()


class CryptoRequest(BaseModel):
    algorithm: str
    operation: str
    text: Optional[str] = None
    key1: Any = None
    key2: Optional[int] = None
    data: Optional[dict] = None


class CryptoResponse(BaseModel):
    result: str
    algorithm: str
    operation: str
    encrypted_key: Optional[str] = None
    private_key: Optional[str] = None


class Server:
    def _parse_hill_matrix(self, key_str: str) -> np.ndarray:
        key_str = (key_str or "").strip()
        if not key_str:
            raise HTTPException(400, "Hill anahtar matrisi boş olamaz")

        if key_str.startswith("["):
            matrix_list = ast.literal_eval(key_str)
        else:
            rows = key_str.split(";")
            matrix_list = [[int(x) for x in row.split()] for row in rows]

        matrix = np.array(matrix_list)
        if matrix.shape[0] != matrix.shape[1]:
            raise HTTPException(400, "Hill matrisi kare olmalı")
        return matrix

    # ---------------- ENCRYPT ----------------
    def encrypt(self, algorithm: str, text: str, key1=None, key2=None):
        try:
            if algorithm == "Caesar":
                cipher = CaesarCipherTR()
                cipher.shift = int(key1)
                return cipher.encrypt(text)

            elif algorithm == "Vigenere":
                return VigenereCipherTR(str(key1)).encrypt(text)

            elif algorithm == "Affine":
                cipher = AffineCipherTR()
                cipher.a = int(key1)
                cipher.b = int(key2)
                return cipher.encrypt(text)

            elif algorithm == "Rail Fence":
                cipher = RailFenceCipherTR()
                cipher.rails = int(key1)
                return cipher.encrypt(text)

            elif algorithm == "Route":
                cipher = RouteCipherTR()
                cipher.cols = int(key1)
                return cipher.encrypt(text)

            elif algorithm == "Columnar":
                cipher = ColumnarCipherTR()
                cipher.key = str(key1)
                return cipher.encrypt(text)

            elif algorithm == "Polybius":
                return PolybiusCipherTR().encrypt(text)

            elif algorithm == "Hill":
                matrix = self._parse_hill_matrix(str(key1))
                return HillCipherTR(matrix).encrypt(text)

            elif algorithm == "AES":
                return AESCipherTR(str(key1)).encrypt(text)

            elif algorithm == "DES":
                return DESCipherTR(str(key1)).encrypt(text)

            # ✅ DÜZELTİLEN KISIM
            elif algorithm == "AES Kütüphaneli":
                aes = AESLibraryCipherTR()
                return aes.encrypt(text)

            elif algorithm == "DES Kütüphaneli":
                des = DESLibraryCipherTR()
                return des.encrypt(text)

            else:
                raise HTTPException(400, "Geçersiz algoritma")

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(400, str(e))

    # ---------------- DECRYPT ----------------
    def decrypt(self, algorithm: str, data: dict, key1=None, key2=None):
        try:
            # ✅ DÜZELTİLEN KISIM
            if algorithm == "AES Kütüphaneli":
                aes = AESLibraryCipherTR()
                return aes.decrypt(data)

            elif algorithm == "DES Kütüphaneli":
                des = DESLibraryCipherTR()
                return des.decrypt(data)

            elif algorithm == "AES":
                return AESCipherTR(str(key1)).decrypt(data)

            elif algorithm == "DES":
                return DESCipherTR(str(key1)).decrypt(data)

            else:
                raise HTTPException(400, "Geçersiz algoritma")

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(400, str(e))


server = Server()


@app.post("/crypto", response_model=CryptoResponse)
async def process_crypto(req: CryptoRequest):

    if req.operation == "encrypt":
        result = server.encrypt(req.algorithm, req.text, req.key1, req.key2)

        if req.algorithm in ["AES Kütüphaneli", "DES Kütüphaneli"]:
            return CryptoResponse(
                result=result["ciphertext"],
                algorithm=req.algorithm,
                operation=req.operation,
                encrypted_key=result["encrypted_key"],
                private_key=result["private_key"]
            )

        return CryptoResponse(
            result=str(result),
            algorithm=req.algorithm,
            operation=req.operation
        )

    elif req.operation == "decrypt":
        if not req.data:
            raise HTTPException(400, "Decrypt için data zorunlu")

        result = server.decrypt(req.algorithm, req.data, req.key1, req.key2)

        return CryptoResponse(
            result=str(result),
            algorithm=req.algorithm,
            operation=req.operation
        )

    else:
        raise HTTPException(400, "Geçersiz işlem")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)