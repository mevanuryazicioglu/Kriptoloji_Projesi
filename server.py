from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
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
import ast
import numpy as np
import traceback
import json
import base64

app = FastAPI()


# ===================== MODELLER =====================

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


# ===================== SERVER =====================

class Server:

    # -------- Hill yardımcıları --------
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
                    nums = [int(x) for x in row.strip().split()]
                    matrix_list.append(nums)

            matrix = np.array(matrix_list)

        except Exception as e:
            raise HTTPException(
                400,
                "Hill anahtar formatı hatalı.\n"
                "Örnekler:\n"
                "  [[3,3],[2,5]]\n"
                "  3 3; 2 5\n"
                f"Gelen: {key_str}\n"
                f"Hata: {e}"
            )

        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise HTTPException(400, "Hill matrisi kare olmalı")

        return matrix

    def _sanitize_hill_text(self, text: str) -> str:
        return text.replace(" ", "").replace("\n", "").replace("\r", "").strip()

    # -------- ENCRYPT --------
    def encrypt(self, algorithm: str, text: str, key1=None, key2=None):
        try:
            if algorithm == "Caesar":
                c = CaesarCipherTR()
                c.shift = int(key1)
                return c.encrypt(text)

            if algorithm == "Vigenere":
                return VigenereCipherTR(str(key1)).encrypt(text)

            if algorithm == "Affine":
                c = AffineCipherTR()
                c.a = int(key1)
                c.b = int(key2)
                return c.encrypt(text)

            if algorithm == "Rail Fence":
                c = RailFenceCipherTR()
                c.rails = int(key1)
                return c.encrypt(text)

            if algorithm == "Route":
                c = RouteCipherTR()
                c.cols = int(key1)
                return c.encrypt(text)

            if algorithm == "Columnar":
                c = ColumnarCipherTR()
                c.key = str(key1)
                return c.encrypt(text)

            if algorithm == "Polybius":
                return PolybiusCipherTR().encrypt(text)

            if algorithm == "Hill":
                matrix = self._parse_hill_matrix(str(key1))
                clean = self._sanitize_hill_text(text)
                return HillCipherTR(matrix).encrypt(clean)

            if algorithm == "AES":
                return AESCipherTR(str(key1)).encrypt(text)

            if algorithm == "DES":
                return DESCipherTR(str(key1)).encrypt(text)

            if algorithm == "AES Kütüphaneli":
                return AESLibraryCipherTR().encrypt(text)

            if algorithm == "DES Kütüphaneli":
                return DESLibraryCipherTR().encrypt(text)

            raise HTTPException(400, "Geçersiz algoritma")

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(400, str(e))

    # -------- DECRYPT --------
    def decrypt(self, algorithm: str, text: Optional[str], data: Optional[dict], key1=None, key2=None):
        try:
            if algorithm == "AES Kütüphaneli":
                if not data:
                    raise HTTPException(400, "AES Kütüphaneli decrypt için data zorunlu")
                return AESLibraryCipherTR().decrypt(data)

            if algorithm == "DES Kütüphaneli":
                if not data:
                    raise HTTPException(400, "DES Kütüphaneli decrypt için data zorunlu")
                return DESLibraryCipherTR().decrypt(data)

            if algorithm == "AES":
                if text is None:
                    raise HTTPException(400, "AES decrypt için text zorunlu")
                return AESCipherTR(str(key1)).decrypt(text)

            if algorithm == "DES":
                if text is None:
                    raise HTTPException(400, "DES decrypt için text zorunlu")
                return DESCipherTR(str(key1)).decrypt(text)

            if algorithm == "Caesar":
                if text is None:
                    raise HTTPException(400, "Caesar decrypt için text zorunlu")
                c = CaesarCipherTR()
                c.shift = int(key1)
                return c.decrypt(text)

            if algorithm == "Vigenere":
                if text is None:
                    raise HTTPException(400, "Vigenere decrypt için text zorunlu")
                return VigenereCipherTR(str(key1)).decrypt(text)

            if algorithm == "Affine":
                if text is None:
                    raise HTTPException(400, "Affine decrypt için text zorunlu")
                c = AffineCipherTR()
                c.a = int(key1)
                c.b = int(key2)
                return c.decrypt(text)

            if algorithm == "Rail Fence":
                if text is None:
                    raise HTTPException(400, "Rail Fence decrypt için text zorunlu")
                c = RailFenceCipherTR()
                c.rails = int(key1)
                return c.decrypt(text)

            if algorithm == "Route":
                if text is None:
                    raise HTTPException(400, "Route decrypt için text zorunlu")
                c = RouteCipherTR()
                c.cols = int(key1)
                return c.decrypt(text)

            if algorithm == "Columnar":
                if text is None:
                    raise HTTPException(400, "Columnar decrypt için text zorunlu")
                c = ColumnarCipherTR()
                c.key = str(key1)
                return c.decrypt(text)

            if algorithm == "Polybius":
                if text is None:
                    raise HTTPException(400, "Polybius decrypt için text zorunlu")
                return PolybiusCipherTR().decrypt(text)

            if algorithm == "Hill":
                if text is None:
                    raise HTTPException(400, "Hill decrypt için text zorunlu")
                matrix = self._parse_hill_matrix(str(key1))
                clean = self._sanitize_hill_text(text)
                return HillCipherTR(matrix).decrypt(clean)

            raise HTTPException(400, "Geçersiz algoritma")

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(400, str(e))

    # -------- DOSYA İŞLEMLERİ --------

    def _is_binary_supported(self, algorithm: str) -> bool:
        # ✅ Binary dosyaları güvenle şifreleyebileceğimiz algoritmalar:
        return algorithm in ["AES", "DES", "AES Kütüphaneli", "DES Kütüphaneli"]

    def _read_file_as_text_or_base64(self, algorithm: str, raw_bytes: bytes) -> dict:
        """
        Dönen dict:
        {
          "mode": "text" veya "base64",
          "content": <string>
        }
        """
        if self._is_binary_supported(algorithm):
            b64 = base64.b64encode(raw_bytes).decode("utf-8")
            return {"mode": "base64", "content": b64}

        # Klasik algoritmalar: sadece UTF-8 metin
        try:
            txt = raw_bytes.decode("utf-8")
        except Exception:
            raise HTTPException(
                400,
                "Bu algoritma için yalnızca UTF-8 metin dosyaları desteklenir. "
                "İkili dosyalar (pdf/jpg/zip) için AES/DES kullan."
            )
        return {"mode": "text", "content": txt}

    def _write_back_bytes(self, mode: str, text: str) -> bytes:
        if mode == "base64":
            return base64.b64decode(text.encode("utf-8"))
        return text.encode("utf-8")


server = Server()


# ===================== MEVCUT ENDPOINT (TEXT) =====================

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

    if req.operation == "decrypt":
        if req.algorithm in ["AES Kütüphaneli", "DES Kütüphaneli"]:
            if not req.data:
                raise HTTPException(400, "Decrypt için data zorunlu")

            if "iv" not in req.data and req.iv:
                req.data["iv"] = req.iv

            if "ciphertext" not in req.data and req.text:
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

    raise HTTPException(400, "Geçersiz işlem")


# ===================== YENİ ENDPOINT: DOSYA ŞİFRELE =====================

@app.post("/crypto/file/encrypt")
async def crypto_file_encrypt(
    algorithm: str = Form(...),
    key1: Optional[str] = Form(None),
    key2: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    raw = await file.read()

    file_payload = server._read_file_as_text_or_base64(algorithm, raw)
    mode = file_payload["mode"]
    content = file_payload["content"]

    # Encrypt çağır
    enc = server.encrypt(algorithm, content, key1, key2)

    package = {
        "package_version": 1,
        "algorithm": algorithm,
        "original_filename": file.filename,
        "content_mode": mode,
        "operation": "encrypt"
    }

    # Kütüphaneli AES/DES dict döndürür
    if algorithm in ["AES Kütüphaneli", "DES Kütüphaneli"]:
        package["ciphertext"] = enc["ciphertext"]
        package["iv"] = enc.get("iv")
        package["encrypted_key"] = enc["encrypted_key"]
        package["private_key"] = enc["private_key"]
    else:
        package["ciphertext"] = str(enc)

    out_bytes = json.dumps(package, ensure_ascii=False, indent=2).encode("utf-8")
    out_name = f"{file.filename}.enc.json"

    return Response(
        content=out_bytes,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{out_name}"'
        }
    )


# ===================== YENİ ENDPOINT: DOSYA DEŞİFRELE =====================

@app.post("/crypto/file/decrypt")
async def crypto_file_decrypt(
    key1: Optional[str] = Form(None),
    key2: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    raw = await file.read()

    try:
        package = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(400, "Deşifre için yüklenen dosya geçerli bir .json paket değil")

    algorithm = package.get("algorithm")
    original_filename = package.get("original_filename", "output.bin")
    mode = package.get("content_mode", "text")
    ciphertext = package.get("ciphertext")

    if not algorithm or ciphertext is None:
        raise HTTPException(400, "Paket bozuk: algorithm veya ciphertext eksik")

    # Decrypt: kütüphaneli algoritmalar data ister
    if algorithm in ["AES Kütüphaneli", "DES Kütüphaneli"]:
        data = {
            "ciphertext": ciphertext,
            "iv": package.get("iv"),
            "encrypted_key": package.get("encrypted_key"),
            "private_key": package.get("private_key"),
        }
        if not data.get("iv"):
            raise HTTPException(400, "Paket bozuk: iv eksik")
        if not data.get("encrypted_key") or not data.get("private_key"):
            raise HTTPException(400, "Paket bozuk: RSA anahtar verileri eksik")

        plain_text = server.decrypt(algorithm, None, data, None, None)

    else:
        # Klasik / manuel AES/DES: key gerektirebilir
        if algorithm in ["AES", "DES", "Caesar", "Vigenere", "Rail Fence", "Route", "Columnar", "Hill", "Affine"]:
            if key1 is None or str(key1).strip() == "":
                raise HTTPException(400, f"{algorithm} decrypt için key1 zorunlu")

        if algorithm == "Affine":
            if key2 is None or str(key2).strip() == "":
                raise HTTPException(400, "Affine decrypt için key2 zorunlu")

        plain_text = server.decrypt(algorithm, ciphertext, None, key1, key2)

    out_bytes = server._write_back_bytes(mode, plain_text)

    return Response(
        content=out_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{original_filename}"',
            "X-Original-Filename": original_filename
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
