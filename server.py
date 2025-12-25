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

    iv: Optional[str] = None


class CryptoResponse(BaseModel):
    result: str
    algorithm: str
    operation: str
    encrypted_key: Optional[str] = None
    private_key: Optional[str] = None

    iv: Optional[str] = None


class Server:
    def _parse_hill_matrix(self, key_str: str) -> np.ndarray:
        key_str = (key_str or "").strip()
        if not key_str:
            raise HTTPException(400, "Hill anahtar matrisi boş olamaz")

      
        normalized = key_str.replace(",", " ").replace("\n", " ").strip()

        try:
            if normalized.startswith("["):
                matrix_list = ast.literal_eval(normalized)

            else:
                rows = normalized.split(";")
                matrix_list = []
                for row in rows:
                    row = row.strip()
                    if not row:
                        continue
                    nums = [int(x) for x in row.split()]
                    matrix_list.append(nums)

            matrix = np.array(matrix_list)

        except Exception as e:
            raise HTTPException(
                400,
                "Hill anahtar formatı hatalı. Örnekler:\n"
                "1) [[3,3],[2,5]]\n"
                "2) 3 3; 2 5\n"
                f"Gelen anahtar: {key_str}\n"
                f"Hata: {e}"
            )
    
        if matrix.ndim != 2:
            raise HTTPException(400, "Hill matrisi 2 boyutlu olmalı (örn. 2x2, 3x3)")

        if matrix.shape[0] != matrix.shape[1]:
            raise HTTPException(400, "Hill matrisi kare olmalı")

        return matrix

    def _sanitize_hill_text(self, text: str) -> str:
        if text is None:
            return ""

        cleaned = text.replace("\n", "").replace("\r", "").replace(" ", "").strip()

   

        return cleaned
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
    def decrypt(self, algorithm: str, text: Optional[str], data: Optional[dict], key1=None, key2=None):
        """
        ✅ Kural:
        - Kütüphaneli AES/DES -> data dict ile çöz
        - Diğerleri -> text (ciphertext) ile çöz
        """
        try:
            if algorithm == "AES Kütüphaneli":
                if not data:
                    raise HTTPException(400, "AES Kütüphaneli decrypt için data zorunlu")
                aes = AESLibraryCipherTR()
                return aes.decrypt(data)

            elif algorithm == "DES Kütüphaneli":
                if not data:
                    raise HTTPException(400, "DES Kütüphaneli decrypt için data zorunlu")
                des = DESLibraryCipherTR()
                return des.decrypt(data)

            elif algorithm == "AES":
                if text is None:
                    raise HTTPException(400, "AES decrypt için text zorunlu")
                return AESCipherTR(str(key1)).decrypt(text)

            elif algorithm == "DES":
                if text is None:
                    raise HTTPException(400, "DES decrypt için text zorunlu")
                return DESCipherTR(str(key1)).decrypt(text)

            elif algorithm == "Caesar":
                if text is None:
                    raise HTTPException(400, "Caesar decrypt için text zorunlu")
                cipher = CaesarCipherTR()
                cipher.shift = int(key1)
                return cipher.decrypt(text)

            elif algorithm == "Vigenere":
                if text is None:
                    raise HTTPException(400, "Vigenere decrypt için text zorunlu")
                return VigenereCipherTR(str(key1)).decrypt(text)

            elif algorithm == "Affine":
                if text is None:
                    raise HTTPException(400, "Affine decrypt için text zorunlu")
                cipher = AffineCipherTR()
                cipher.a = int(key1)
                cipher.b = int(key2)
                return cipher.decrypt(text)

            elif algorithm == "Rail Fence":
                if text is None:
                    raise HTTPException(400, "Rail Fence decrypt için text zorunlu")
                cipher = RailFenceCipherTR()
                cipher.rails = int(key1)
                return cipher.decrypt(text)

            elif algorithm == "Route":
                if text is None:
                    raise HTTPException(400, "Route decrypt için text zorunlu")
                cipher = RouteCipherTR()
                cipher.cols = int(key1)
                return cipher.decrypt(text)

            elif algorithm == "Columnar":
                if text is None:
                    raise HTTPException(400, "Columnar decrypt için text zorunlu")
                cipher = ColumnarCipherTR()
                cipher.key = str(key1)
                return cipher.decrypt(text)

            elif algorithm == "Polybius":
                if text is None:
                    raise HTTPException(400, "Polybius decrypt için text zorunlu")
                return PolybiusCipherTR().decrypt(text)

            elif algorithm == "Hill":
                if text is None:
                    raise HTTPException(400, "Hill decrypt için text zorunlu")
                matrix = self._parse_hill_matrix(str(key1))
                return HillCipherTR(matrix).decrypt(text)

            else:
                raise HTTPException(400, "Geçersiz algoritma")

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(400, str(e))


server = Server()


@app.post("/crypto", response_model=CryptoResponse)
async def process_crypto(req: CryptoRequest):

    if req.operation == "encrypt":
        if req.text is None:
            raise HTTPException(400, "Encrypt için text zorunlu")

        result = server.encrypt(req.algorithm, req.text, req.key1, req.key2)

        if req.algorithm in ["AES Kütüphaneli", "DES Kütüphaneli"]:
            return CryptoResponse(
                result=result["ciphertext"],
                algorithm=req.algorithm,
                operation=req.operation,
                encrypted_key=result["encrypted_key"],
                private_key=result["private_key"],
                iv=result.get("iv")
            )

        return CryptoResponse(
            result=str(result),
            algorithm=req.algorithm,
            operation=req.operation
        )

    elif req.operation == "decrypt":
    
        if req.algorithm in ["AES Kütüphaneli", "DES Kütüphaneli"]:
            if not req.data:
                raise HTTPException(400, "Decrypt için data zorunlu")

            if req.data is not None and "iv" not in req.data and req.iv:
                req.data["iv"] = req.iv

            if req.data is not None and "ciphertext" not in req.data and req.text:
                req.data["ciphertext"] = req.text

            result = server.decrypt(req.algorithm, req.text, req.data, req.key1, req.key2)

        else:
            if req.text is None:
                raise HTTPException(400, "Decrypt için text zorunlu")
            result = server.decrypt(req.algorithm, req.text, None, req.key1, req.key2)

        return CryptoResponse(
            result=str(result),
            algorithm=req.algorithm,
            operation=req.operation
        )

    else:
        raise HTTPException(400, "Geçersiz işlem")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
