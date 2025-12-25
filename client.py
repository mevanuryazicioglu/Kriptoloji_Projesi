import tkinter as tk
import requests

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
    def __init__(self, title, operation_type):
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("500x550")
        self.operation_type = operation_type

        # 🔥 Decrypt için saklanan veri
        self.last_crypto_data = None

        tk.Label(self.window, text="Metin Girin:", font=("Arial", 9)).pack(pady=(10, 5))
        self.input_text = tk.Entry(self.window, width=60)
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

        tk.Label(self.window, text="Sonuç:", font=("Arial", 9)).pack(pady=(10, 3))

        self.result_text = tk.Text(self.window, height=10, wrap="word")
        self.result_text.pack(padx=10, pady=5, fill="both", expand=True)
        self.result_text.config(state="disabled")

        tk.Button(
            self.window,
            text="Şifrele" if operation_type == "encrypt" else "Deşifrele",
            width=20,
            command=self.process_text
        ).pack(pady=5)

        tk.Button(self.window, text="Temizle", width=20, command=self.clear_fields).pack(pady=5)

    def update_keys(self, *args):
        algo = self.algorithm.get()
        self.key1_label.pack_forget()
        self.key1_entry.pack_forget()
        self.key1_entry.delete(0, tk.END)

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
            self.key1_label.config(text="Anahtar 1")
            set_placeholder(self.key1_entry, "Sayı girin")
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

    def set_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def process_text(self):
        algo = self.algorithm.get()

        if not algo:
            self.set_result("Hata: Algoritma seçilmedi")
            return

        # 🔐 AES/DES Kütüphaneli DECRYPT
        if algo in ["AES Kütüphaneli", "DES Kütüphaneli"] and self.operation_type == "decrypt":
            if not self.last_crypto_data:
                self.set_result("Hata: Önce şifreleme yapmalısın")
                return

            payload = {
                "algorithm": algo,
                "operation": "decrypt",
                "data": self.last_crypto_data
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

            if algo not in ["AES Kütüphaneli", "DES Kütüphaneli", "Polybius"]:
                key = self.key1_entry.get().strip()
                if not key or "gir" in key:
                    self.set_result("Hata: Anahtar eksik")
                    return
                payload["key1"] = key

        try:
            response = requests.post(f"{SERVER_URL}/crypto", json=payload)
            data = response.json()

            if response.status_code == 200:
                # 🔥 AES/DES encrypt
                if algo in ["AES Kütüphaneli", "DES Kütüphaneli"] and self.operation_type == "encrypt":
                    self.last_crypto_data = {
                        "ciphertext": data["result"],
                        "encrypted_key": data["encrypted_key"],
                        "private_key": data["private_key"]
                    }

                    self.set_result(
                        "ŞİFRELİ METİN:\n"
                        + data["result"]
                        + "\n\nDeşifreleme için hazır."
                    )
                else:
                    self.set_result("Sonuç:\n" + data["result"])
            else:
                self.set_result("Hata:\n" + data.get("detail", "Bilinmeyen hata"))

        except Exception as e:
            self.set_result(f"Sunucu hatası: {e}")

    def clear_fields(self):
        self.input_text.delete(0, tk.END)
        self.key1_entry.delete(0, tk.END)
        self.set_result("")
        self.last_crypto_data = None


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    CryptoWindow("Şifreleme", "encrypt")
    CryptoWindow("Deşifreleme", "decrypt")

    root.mainloop()