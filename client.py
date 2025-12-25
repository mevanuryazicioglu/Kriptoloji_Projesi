import tkinter as tk
from tkinter import filedialog
import requests
import os

SERVER_URL = "http://127.0.0.1:8000"


def set_placeholder(entry, text):
    try:
        entry.unbind("<FocusIn>")
        entry.unbind("<FocusOut>")
    except:
        pass

    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.config(fg='gray')

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg='gray')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


class CryptoWindow:
    shared_crypto_data = None

    def __init__(self, title, operation_type):
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("520x620")
        self.operation_type = operation_type

        self.last_crypto_data = None

        tk.Label(self.window, text="Metin Girin:", font=("Arial", 9)).pack(pady=(10, 5))
        self.input_text = tk.Entry(self.window, width=62)
        self.input_text.pack(pady=5)

        tk.Label(self.window, text="Algoritma Seç:").pack(pady=5)
        self.algorithm = tk.StringVar(value="")
        tk.OptionMenu(
            self.window,
            self.algorithm,
            "Caesar",
            "Affine",
            "Vigenere",
            "Rail Fence",
            "Route",
            "Columnar",
            "Polybius",
            "Hill",
            "DES",
            "AES",
            "AES Kütüphaneli",
            "DES Kütüphaneli"
        ).pack(pady=5)

        self.algorithm.trace("w", self.update_keys)

        self.key_frame = tk.Frame(self.window)
        self.key_frame.pack(pady=5)

        self.key1_label = tk.Label(self.key_frame, text="", font=("Arial", 8))
        self.key1_entry = tk.Entry(self.key_frame, width=50)

        self.key2_label = tk.Label(self.key_frame, text="", font=("Arial", 8))
        self.key2_entry = tk.Entry(self.key_frame, width=50)

        tk.Label(self.window, text="Sonuç:", font=("Arial", 9)).pack(pady=(10, 3))

        self.result_text = tk.Text(self.window, height=10, wrap="word")
        self.result_text.pack(padx=10, pady=5, fill="both", expand=True)
        self.result_text.config(state="disabled")

        # Metin şifreleme/deşifreleme butonu
        tk.Button(
            self.window,
            text="Şifrele" if operation_type == "encrypt" else "Deşifrele",
            width=22,
            command=self.process_text
        ).pack(pady=5)

        tk.Button(self.window, text="Temizle", width=22, command=self.clear_fields).pack(pady=5)

        # ✅ Dosya butonları (pencereye göre ayrı)
        tk.Label(self.window, text="Dosya İşlemleri:", font=("Arial", 9)).pack(pady=(12, 4))

        if self.operation_type == "encrypt":
            tk.Button(
                self.window,
                text="Dosya Şifrele (Yükle)",
                width=22,
                command=self.encrypt_file
            ).pack(pady=4)

        if self.operation_type == "decrypt":
            tk.Button(
                self.window,
                text="Dosya Deşifrele (Paket Yükle)",
                width=22,
                command=self.decrypt_file
            ).pack(pady=4)

    def update_keys(self, *args):
        algo = self.algorithm.get()

        self.key1_label.pack_forget()
        self.key1_entry.pack_forget()
        self.key2_label.pack_forget()
        self.key2_entry.pack_forget()

        self.key1_entry.delete(0, tk.END)
        self.key2_entry.delete(0, tk.END)

        if not algo or algo == "Polybius":
            return

        if algo in ["AES Kütüphaneli", "DES Kütüphaneli"]:
            return

        self.key1_label.pack()
        self.key1_entry.pack(pady=2)

        if algo == "Caesar":
            self.key1_label.config(text="Anahtar (Sayı)")
            set_placeholder(self.key1_entry, "Sayı girin")

        elif algo == "Affine":
            self.key1_label.config(text="Anahtar a")
            set_placeholder(self.key1_entry, "Örn: 5")

            self.key2_label.pack()
            self.key2_entry.pack(pady=2)
            self.key2_label.config(text="Anahtar b")
            set_placeholder(self.key2_entry, "Örn: 8")

        elif algo == "Vigenere":
            self.key1_label.config(text="Anahtar Kelime")
            set_placeholder(self.key1_entry, "Kelime girin")

        elif algo == "Rail Fence":
            self.key1_label.config(text="Ray Sayısı")
            set_placeholder(self.key1_entry, "Sayı girin")

        elif algo == "Route":
            self.key1_label.config(text="Sütun Sayısı")
            set_placeholder(self.key1_entry, "Sayı girin")

        elif algo == "Columnar":
            self.key1_label.config(text="Anahtar Kelime")
            set_placeholder(self.key1_entry, "Kelime girin")

        elif algo == "Hill":
            self.key1_label.config(text="Anahtar Matris")
            set_placeholder(self.key1_entry, "[[3,3],[2,5]]")

        elif algo == "DES":
            self.key1_label.config(text="DES Anahtarı (8 karakter)")
            set_placeholder(self.key1_entry, "Örn: 12345678")

        elif algo == "AES":
            self.key1_label.config(text="AES Anahtarı (16/24/32 karakter)")
            set_placeholder(self.key1_entry, "Örn: 1234567890abcdef")

    def set_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def _get_keys_for_algo(self, algo: str):
        key1 = None
        key2 = None

        if algo in ["AES Kütüphaneli", "DES Kütüphaneli", "Polybius"]:
            return key1, key2

        if algo in ["Caesar", "Vigenere", "Rail Fence", "Route", "Columnar", "Hill", "DES", "AES", "Affine"]:
            key1 = self.key1_entry.get().strip()
            if not key1 or "gir" in key1:
                raise ValueError("Hata: Anahtar eksik (key1)")

        if algo == "Affine":
            key2 = self.key2_entry.get().strip()
            if not key2 or "gir" in key2:
                raise ValueError("Hata: Affine için 2. anahtar (key2) eksik")

        return key1, key2

    # ---------------- METİN İŞLEMLERİ ----------------

    def process_text(self):
        algo = self.algorithm.get()

        if not algo:
            self.set_result("Hata: Algoritma seçilmedi")
            return

        if algo in ["AES Kütüphaneli", "DES Kütüphaneli"] and self.operation_type == "decrypt":
            if not self.last_crypto_data and CryptoWindow.shared_crypto_data:
                self.last_crypto_data = CryptoWindow.shared_crypto_data

            if not self.last_crypto_data:
                self.set_result("Hata: Önce şifreleme yapmalısın (kütüphaneli decrypt için RSA anahtar verisi gerekli)")
                return

            typed_text = self.input_text.get().strip()
            ciphertext_to_use = typed_text if typed_text else self.last_crypto_data.get("ciphertext", "")

            if "iv" not in self.last_crypto_data or not self.last_crypto_data.get("iv"):
                self.set_result("Hata: Kütüphaneli decrypt için 'iv' eksik")
                return

            payload = {
                "algorithm": algo,
                "operation": "decrypt",
                "text": ciphertext_to_use,
                "data": self.last_crypto_data,
                "iv": self.last_crypto_data.get("iv")
            }

        else:
            text = self.input_text.get()
            if not text.strip():
                self.set_result("Hata: Metin boş olamaz")
                return

            payload = {
                "algorithm": algo,
                "operation": self.operation_type,
                "text": text
            }

            try:
                key1, key2 = self._get_keys_for_algo(algo)
                if key1 is not None:
                    payload["key1"] = key1
                if key2 is not None:
                    payload["key2"] = int(key2) if algo == "Affine" else key2
            except Exception as e:
                self.set_result(str(e))
                return

        try:
            response = requests.post(f"{SERVER_URL}/crypto", json=payload)

            try:
                data = response.json()
            except Exception:
                self.set_result(
                    "Hata: Sunucu JSON dönmedi.\n\n"
                    f"HTTP: {response.status_code}\n"
                    f"Yanıt:\n{response.text}"
                )
                return

            if response.status_code == 200:
                if algo in ["AES Kütüphaneli", "DES Kütüphaneli"] and self.operation_type == "encrypt":
                    self.last_crypto_data = {
                        "ciphertext": data.get("result"),
                        "encrypted_key": data.get("encrypted_key"),
                        "private_key": data.get("private_key"),
                        "iv": data.get("iv")
                    }
                    CryptoWindow.shared_crypto_data = self.last_crypto_data

                    self.set_result(
                        "ŞİFRELİ METİN:\n"
                        + str(data.get("result"))
                        + "\n\nDeşifreleme için hazır."
                    )
                else:
                    self.set_result("Sonuç:\n" + str(data.get("result")))
            else:
                detail = data.get("detail", "Bilinmeyen hata")
                self.set_result(
                    "Hata:\n"
                    + str(detail)
                    + f"\n\nHTTP: {response.status_code}\n"
                    + "Sunucu Yanıtı (raw):\n"
                    + response.text
                )

        except Exception as e:
            self.set_result(f"Sunucu hatası: {e}")

    # ---------------- DOSYA ŞİFRELE (SADECE ENCRYPT PENCERESİ) ----------------

    def encrypt_file(self):
        algo = self.algorithm.get()
        if not algo:
            self.set_result("Hata: Dosya için algoritma seçmelisin")
            return

        file_path = filedialog.askopenfilename(title="Şifrelenecek dosyayı seç")
        if not file_path:
            return

        key1 = None
        key2 = None
        try:
            key1, key2 = self._get_keys_for_algo(algo)
        except Exception as e:
            if algo not in ["AES Kütüphaneli", "DES Kütüphaneli", "Polybius"]:
                self.set_result(str(e))
                return

        default_out = file_path + ".enc.json"
        out_path = filedialog.asksaveasfilename(
            title="Şifreli paket dosyasını kaydet",
            defaultextension=".json",
            initialfile=os.path.basename(default_out),
            filetypes=[("Encrypted Package", "*.json"), ("All Files", "*.*")]
        )
        if not out_path:
            return

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
                data = {"algorithm": algo}
                if key1 is not None:
                    data["key1"] = key1
                if key2 is not None:
                    data["key2"] = key2

                r = requests.post(f"{SERVER_URL}/crypto/file/encrypt", files=files, data=data)

            if r.status_code != 200:
                self.set_result(f"Hata: {r.status_code}\n{r.text}")
                return

            with open(out_path, "wb") as out:
                out.write(r.content)

            self.set_result(f"Dosya şifrelendi.\nKaydedildi:\n{out_path}")

        except Exception as e:
            self.set_result(f"Sunucu/Dosya hatası: {e}")

    # ---------------- DOSYA DEŞİFRELE (SADECE DECRYPT PENCERESİ) ----------------

    def decrypt_file(self):
        pack_path = filedialog.askopenfilename(
            title="Deşifrelenecek paket (.enc.json) dosyasını seç",
            filetypes=[("Encrypted Package", "*.json"), ("All Files", "*.*")]
        )
        if not pack_path:
            return

        # Manuel/Klasik decrypt için key gerekebilir -> UI'dan alırız
        algo = self.algorithm.get()
        key1 = None
        key2 = None
        try:
            if algo:
                key1, key2 = self._get_keys_for_algo(algo)
        except:
            key1, key2 = None, None

        out_path = filedialog.asksaveasfilename(
            title="Çözülmüş dosyayı kaydet",
            defaultextension="",
            initialfile="decrypted_output",
            filetypes=[("All Files", "*.*")]
        )
        if not out_path:
            return

        try:
            with open(pack_path, "rb") as f:
                files = {"file": (os.path.basename(pack_path), f, "application/json")}
                data = {}
                if key1 is not None:
                    data["key1"] = key1
                if key2 is not None:
                    data["key2"] = key2

                r = requests.post(f"{SERVER_URL}/crypto/file/decrypt", files=files, data=data)

            if r.status_code != 200:
                self.set_result(f"Hata: {r.status_code}\n{r.text}")
                return

            with open(out_path, "wb") as out:
                out.write(r.content)

            self.set_result(f"Dosya deşifrelendi.\nKaydedildi:\n{out_path}")

        except Exception as e:
            self.set_result(f"Sunucu/Dosya hatası: {e}")

    def clear_fields(self):
        self.input_text.delete(0, tk.END)
        self.key1_entry.delete(0, tk.END)
        self.key2_entry.delete(0, tk.END)
        self.set_result("")
        self.last_crypto_data = None
        CryptoWindow.shared_crypto_data = None


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    CryptoWindow("Şifreleme", "encrypt")
    CryptoWindow("Deşifreleme", "decrypt")

    root.mainloop()
