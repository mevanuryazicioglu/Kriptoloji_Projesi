import tkinter as tk
import requests

SERVER_URL = "http://127.0.0.1:8000"

def set_placeholder(entry, text):
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

class CryptoGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Kriptoloji Projesi")
        self.window.geometry("450x400")

        tk.Label(self.window, text="Metin Girin:", font=("Arial", 9)).pack(pady=(10,5))
        self.input_text = tk.Entry(self.window, width=50)
        self.input_text.pack(pady=5)

        tk.Label(self.window, text="Algoritma Seç:").pack(pady=5)
        self.algorithm = tk.StringVar(value="")
        tk.OptionMenu(self.window, self.algorithm, "Caesar", "Affine", "Vigenere").pack(pady=5)
        self.algorithm.trace("w", self.update_keys)

        self.key_frame = tk.Frame(self.window)
        self.key_frame.pack(pady=5)

        self.key1_label = tk.Label(self.key_frame, text="", font=("Arial", 8), fg="gray")
        self.key1_entry = tk.Entry(self.key_frame, width=20)
        self.key2_label = tk.Label(self.key_frame, text="Sayı girin", font=("Arial", 8), fg="gray")
        self.key2_entry = tk.Entry(self.key_frame, width=20)

        self.result_label = tk.Label(self.window, text="", wraplength=400)
        self.result_label.pack(pady=10)

        tk.Button(self.window, text="Şifrele", width=20, command=self.encrypt_text).pack(pady=5)
        tk.Button(self.window, text="Çöz", width=20, command=self.decrypt_text).pack(pady=5)
        tk.Button(self.window, text="Temizle", width=20, command=self.clear_fields).pack(pady=5)

        self.window.mainloop()

    def update_keys(self, *args):
        algo = self.algorithm.get()
        self.key1_label.pack_forget()
        self.key1_entry.pack_forget()
        self.key2_label.pack_forget()
        self.key2_entry.pack_forget()
        self.key1_entry.delete(0, tk.END)
        self.key2_entry.delete(0, tk.END)

        if algo:
            self.key1_label.pack()
            self.key1_entry.pack(pady=2)
            if algo == "Caesar":
                self.key1_label.config(text="Anahtar 1")
                set_placeholder(self.key1_entry, "Sayı girin")
            elif algo == "Affine":
                self.key1_label.config(text="Anahtar 1")
                set_placeholder(self.key1_entry, "Sayı girin")
                self.key2_label.pack()
                self.key2_entry.pack(pady=2)
                self.key2_label.config(text="Anahtar 2")
                set_placeholder(self.key2_entry, "Sayı girin")
            elif algo == "Vigenere":
                self.key1_label.config(text="Anahtar 1")
                set_placeholder(self.key1_entry, "Kelime girin")

    def encrypt_text(self):
        text = self.input_text.get()
        algo = self.algorithm.get()
        try:
            if not algo:
                self.result_label.config(text="Hata: Algoritma seçilmedi!")
                return
            
            if not text or text.strip() == "":
                self.result_label.config(text="Hata: Metin alanı boş olamaz!")
                return
            
            payload = {
                "algorithm": algo,
                "operation": "encrypt",
                "text": text
            }
            
            if algo == "Caesar":
                key1_str = self.key1_entry.get()
                if not key1_str or key1_str.strip() == "" or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                key1 = int(key1_str)
                payload["key1"] = key1
            elif algo == "Affine":
                key1_str = self.key1_entry.get()
                key2_str = self.key2_entry.get()
                if not key1_str or key1_str.strip() == "" or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                if not key2_str or key2_str.strip() == "" or key2_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 2 boş olamaz!")
                    return
                key1 = int(key1_str)
                key2 = int(key2_str)
                payload["key1"] = key1
                payload["key2"] = key2
            elif algo == "Vigenere":
                key1 = self.key1_entry.get()
                if not key1 or key1.strip() == "" or key1 == "Kelime girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                payload["key1"] = key1
            
            response = requests.post(f"{SERVER_URL}/crypto", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                result = data["result"]
            else:
                result = f"Hata: {response.json().get('detail', 'Bilinmeyen hata')}"
        except requests.exceptions.ConnectionError:
            result = "Hata: Sunucuya bağlanılamadı. Sunucunun çalıştığından emin olun."
        except Exception as e:
            result = f"Hata: {e}"
        self.result_label.config(text=result)

    def decrypt_text(self):
        text = self.input_text.get()
        algo = self.algorithm.get()
        try:
            if not algo:
                self.result_label.config(text="Hata: Algoritma seçilmedi!")
                return
            
            if not text or text.strip() == "":
                self.result_label.config(text="Hata: Metin alanı boş olamaz!")
                return
            
            payload = {
                "algorithm": algo,
                "operation": "decrypt",
                "text": text
            }
            
            if algo == "Caesar":
                key1_str = self.key1_entry.get()
                if not key1_str or key1_str.strip() == "" or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                key1 = int(key1_str)
                payload["key1"] = key1
            elif algo == "Affine":
                key1_str = self.key1_entry.get()
                key2_str = self.key2_entry.get()
                if not key1_str or key1_str.strip() == "" or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                if not key2_str or key2_str.strip() == "" or key2_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 2 boş olamaz!")
                    return
                key1 = int(key1_str)
                key2 = int(key2_str)
                payload["key1"] = key1
                payload["key2"] = key2
            elif algo == "Vigenere":
                key1 = self.key1_entry.get()
                if not key1 or key1.strip() == "" or key1 == "Kelime girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                payload["key1"] = key1
            
            response = requests.post(f"{SERVER_URL}/crypto", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                result = data["result"]
            else:
                result = f"Hata: {response.json().get('detail', 'Bilinmeyen hata')}"
        except requests.exceptions.ConnectionError:
            result = "Hata: Sunucuya bağlanılamadı. Sunucunun çalıştığından emin olun."
        except Exception as e:
            result = f"Hata: {e}"
        self.result_label.config(text=result)

    def clear_fields(self):
        self.input_text.delete(0, tk.END)
        self.key1_entry.delete(0, tk.END)
        self.key2_entry.delete(0, tk.END)
        self.result_label.config(text="")

if __name__ == "__main__":
    CryptoGUI()
