import tkinter as tk
from algorithms.rsa import RSACipherTR
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

class CryptoWindow:
    def __init__(self, title, operation_type, rsa_keys_manager=None):
        self.window = tk.Tk() if rsa_keys_manager is None else tk.Toplevel() # Sadece ilk pencere Tk() diğerleri Toplevel()
        self.window.title(title)
        self.window.geometry("500x550")
        self.operation_type = operation_type
        self.rsa_keys_manager = rsa_keys_manager # Anahtar paylaşımı için

        tk.Label(self.window, text="Metin Girin:", font=("Arial", 9)).pack(pady=(10,5))
        self.input_text = tk.Entry(self.window, width=60)
        self.input_text.pack(pady=5)

        tk.Label(self.window, text="Algoritma Seç:").pack(pady=5)
        self.algorithm = tk.StringVar(value="")
        tk.OptionMenu(self.window, self.algorithm, "Caesar", "Affine", "Vigenere", "Rail Fence", "Route", "Columnar", "Polybius", "Hill", "DES", "AES", "AES Kütüphaneli", "RSA", "DES Kütüphaneli").pack(pady=5)
        self.algorithm.trace("w", self.update_keys)

        self.key_frame = tk.Frame(self.window)
        self.key_frame.pack(pady=5)

        self.key1_label = tk.Label(self.key_frame, text="", font=("Arial", 8))
        self.key1_entry = tk.Entry(self.key_frame, width=50)
        self.key2_label = tk.Label(self.key_frame, text="", font=("Arial", 8))
        self.key2_entry = tk.Entry(self.key_frame, width=50)
        
        self.result_label = tk.Label(self.window, text="", wraplength=450)
        self.result_label.pack(pady=10)

        if self.operation_type == "encrypt":
            tk.Button(self.window, text="Şifrele", width=20, command=self.process_text).pack(pady=5)
        else: # decrypt
            tk.Button(self.window, text="Deşifrele", width=20, command=self.process_text).pack(pady=5)
        
        tk.Button(self.window, text="Temizle", width=20, command=self.clear_fields).pack(pady=5)

        if self.rsa_keys_manager is None: # Ana pencere ise mainloop'u başlat
            self.window.mainloop()

    def update_keys(self, *args):
        algo = self.algorithm.get()
        self.key1_label.pack_forget()
        self.key1_entry.pack_forget()
        self.key2_label.pack_forget()
        self.key2_entry.pack_forget()
        self.key1_entry.delete(0, tk.END)
        self.key2_entry.delete(0, tk.END)
        
        if not algo:
            return

        if algo == "Polybius":
            return

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
            elif algo == "Rail Fence":
                self.key1_label.config(text="Ray")
                set_placeholder(self.key1_entry, "Sayı girin")
            elif algo == "Route":
                self.key1_label.config(text="Sütun sayısı")
                set_placeholder(self.key1_entry, "Sayı girin")
            elif algo == "Columnar":
                self.key1_label.config(text="Anahtar Kelime")
                set_placeholder(self.key1_entry, "Kelime girin")
            elif algo == "Hill":
                self.key1_label.pack()
                self.key1_entry.pack(pady=2)
                self.key1_label.config(text="Anahtar Matris (örn: [[3,3],[2,5]] veya [[6,24,1],[13,16,10],[20,17,15]])")
                set_placeholder(self.key1_entry, "2x2 veya 3x3 matrisi girin (köşeli parantezler ve virgüllerle)")
            elif algo == "DES":
                self.key1_label.pack()
                self.key1_entry.pack(pady=2)
                self.key1_label.config(text="Anahtar (8 karakter)")
                set_placeholder(self.key1_entry, "8 karakter girin")
            elif algo == "AES":
                self.key1_label.pack()
                self.key1_entry.pack(pady=2)
                self.key1_label.config(text="Anahtar (16/24/32 karakter)")
                set_placeholder(self.key1_entry, "16, 24 veya 32 karakter girin")
            elif algo == "AES Kütüphaneli":
                self.key1_label.pack()
                self.key1_entry.pack(pady=2)
                self.key1_label.config(text="Anahtar (16/24/32 karakter)")
                set_placeholder(self.key1_entry, "16, 24 veya 32 karakter girin")
            elif algo == "DES Kütüphaneli":
                self.key1_label.pack()
                self.key1_entry.pack(pady=2)
                self.key1_label.config(text="Anahtar (8 karakter)")
                set_placeholder(self.key1_entry, "8 karakter girin")
            elif algo == "RSA":
                self.key1_label.pack()
                self.key1_entry.pack(pady=2)
                if self.operation_type == "encrypt":
                    self.key1_label.config(text="RSA Açık Anahtar (isteğe bağlı)")
                    set_placeholder(self.key1_entry, "Şifreleme için açık anahtar girin (örn: {'e':..., 'n':...})")
                else: # decrypt
                    self.key1_label.config(text="RSA Özel Anahtar")
                    set_placeholder(self.key1_entry, "Deşifreleme için özel anahtar girin (örn: {'d':..., 'n':...})")

    def process_text(self):
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
                "operation": self.operation_type,
                "text": text
            }
            
            # Anahtar parametrelerini payload'a ekle
            key1_str = self.key1_entry.get().strip()
            key2_str = self.key2_entry.get().strip()

            if algo == "Caesar":
                if not key1_str or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                payload["key1"] = int(key1_str)
            elif algo == "Affine":
                if not key1_str or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                if not key2_str or key2_str == "Sayı girin":
                    self.result_label.config(text="Hata: Anahtar 2 boş olamaz!")
                    return
                payload["key1"] = int(key1_str)
                payload["key2"] = int(key2_str)
            elif algo == "Vigenere":
                if not key1_str or key1_str == "Kelime girin":
                    self.result_label.config(text="Hata: Anahtar 1 boş olamaz!")
                    return
                payload["key1"] = key1_str
            elif algo == "Rail Fence":
                if not key1_str or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Ray sayısı boş olamaz!")
                    return
                payload["key1"] = int(key1_str)
            elif algo == "Route":
                if not key1_str or key1_str == "Sayı girin":
                    self.result_label.config(text="Hata: Sütun sayısı boş olamaz!")
                    return
                payload["key1"] = int(key1_str)
            elif algo == "Columnar":
                if not key1_str or key1_str == "Kelime girin":
                    self.result_label.config(text="Hata: Anahtar kelime boş olamaz!")
                    return
                payload["key1"] = key1_str
            elif algo == "Hill":
                if not key1_str or key1_str == "2x2 veya 3x3 matrisi girin":
                    self.result_label.config(text="Hata: Anahtar matris boş olamaz!")
                    return
                payload["key1"] = key1_str
            elif algo == "DES":
                if not key1_str or key1_str == "8 karakter girin":
                    self.result_label.config(text="Hata: Anahtar boş olamaz ve 8 karakter olmalı!")
                    return
                if len(key1_str) != 8:
                    self.result_label.config(text="Hata: DES anahtarı 8 karakter olmalıdır!")
                    return
                payload["key1"] = key1_str
            elif algo == "AES":
                if not key1_str or key1_str == "16, 24 veya 32 karakter girin":
                    self.result_label.config(text="Hata: AES anahtarı boş olamaz ve 16, 24 veya 32 karakter olmalı!")
                    return
                if len(key1_str) not in [16, 24, 32]:
                    self.result_label.config(text="Hata: AES anahtarı yalnızca 16, 24 veya 32 karakter olabilir!")
                    return
                payload["key1"] = key1_str
            elif algo == "AES Kütüphaneli":
                if not key1_str or key1_str == "16, 24 veya 32 karakter girin":
                    self.result_label.config(text="Hata: AES Kütüphaneli anahtarı boş olamaz ve 16, 24 veya 32 karakter olmalı!")
                    return
                if len(key1_str) not in [16, 24, 32]:
                    self.result_label.config(text="Hata: AES Kütüphaneli anahtarı yalnızca 16, 24 veya 32 karakter olabilir!")
                    return
                payload["key1"] = key1_str
            elif algo == "DES Kütüphaneli":
                if not key1_str or key1_str == "8 karakter girin":
                    self.result_label.config(text="Hata: DES Kütüphaneli anahtarı boş olamaz ve 8 karakter olmalı!")
                    return
                if len(key1_str) != 8:
                    self.result_label.config(text="Hata: DES Kütüphaneli anahtarı 8 karakter olmalıdır!")
                    return
                payload["key1"] = key1_str
            elif algo == "RSA":
                if self.operation_type == "encrypt":
                    if key1_str and key1_str != "Şifreleme için açık anahtar girin (örn: {'e':..., 'n':...})":
                        try:
                            payload["rsa_public_key"] = eval(key1_str)
                        except Exception:
                            self.result_label.config(text="Hata: Geçersiz RSA genel anahtar formatı.")
                            return
                else: # decrypt
                    if not key1_str or key1_str == "Deşifreleme için özel anahtar girin (örn: {'d':..., 'n':...})":
                         self.result_label.config(text="Hata: RSA deşifreleme için özel anahtar boş olamaz!")
                         return
                    try:
                        payload["rsa_private_key"] = eval(key1_str)
                    except Exception:
                        self.result_label.config(text="Hata: Geçersiz RSA özel anahtar formatı.")
                        return
                    
            response = requests.post(f"{SERVER_URL}/crypto", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                result = data["result"]
                if algo == "RSA":
                    if self.operation_type == "encrypt":
                        public_key = data.get("public_key")
                        private_key = data.get("private_key")
                        if public_key and private_key and self.rsa_keys_manager:
                            self.rsa_keys_manager.set_keys(public_key, private_key)
                        self.result_label.config(text=f"Şifrelenmiş Metin: {result}\nAçık Anahtar: {public_key}\nÖzel Anahtar: {private_key}")
                    else: # decrypt
                        self.result_label.config(text=f"Deşifrelenmiş Metin: {result}")
                else:
                    self.result_label.config(text=f"Sonuç: {result}")
            else:
                error_detail = response.json().get('detail', 'Bilinmeyen hata')
                self.result_label.config(text=f"Hata: {error_detail}")
        except requests.exceptions.ConnectionError:
            self.result_label.config(text="Hata: Sunucuya bağlanılamadı. Sunucunun çalıştığından emin olun.")
        except Exception as e:
            self.result_label.config(text=f"Uygulama Hatası: {e}")

    def clear_fields(self):
        self.input_text.delete(0, tk.END)
        self.key1_entry.delete(0, tk.END)
        self.key2_entry.delete(0, tk.END)
        self.result_label.config(text="")

class RSAKeyManager:
    def __init__(self):
        self._public_key = None
        self._private_key = None

    def set_keys(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key

    def get_public_key(self):
        return self._public_key

    def get_private_key(self):
        return self._private_key

# Main execution block to open both windows directly
if __name__ == "__main__":
    # Kök Tkinter penceresini oluştur (gizli kalacak)
    root = tk.Tk()
    root.withdraw() # Ana pencereyi gizle

    rsa_keys_manager_instance = RSAKeyManager()

    # Şifreleme penceresini aç
    encrypt_window = CryptoWindow("Şifreleme", "encrypt", rsa_keys_manager_instance)

    # Deşifreleme penceresini aç
    decrypt_window = CryptoWindow("Deşifreleme", "decrypt", rsa_keys_manager_instance)

    root.mainloop() # Ana Tkinter olay döngüsünü başlat