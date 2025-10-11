import tkinter as tk

TURKISH_ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
ALPHABET_SIZE = len(TURKISH_ALPHABET)

class CaesarCipherTR:
    def __init__(self, key):
        self.key = key % ALPHABET_SIZE

    def encrypt(self, plaintext):
        result = ""
        for c in plaintext.upper():
            if c in TURKISH_ALPHABET:
                idx = (TURKISH_ALPHABET.index(c) + self.key) % ALPHABET_SIZE
                result += TURKISH_ALPHABET[idx]
            else:
                result += c
        return result

    def decrypt(self, ciphertext):
        result = ""
        for c in ciphertext.upper():
            if c in TURKISH_ALPHABET:
                idx = (TURKISH_ALPHABET.index(c) - self.key) % ALPHABET_SIZE
                result += TURKISH_ALPHABET[idx]
            else:
                result += c
        return result

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError(f"Mod inverse yok: a={a}, m={m}")

class AffineCipherTR:
    def __init__(self, a, b):
        if gcd(a, ALPHABET_SIZE) != 1:
            raise ValueError(f"a ve alfabe boyutu coprime olmalı: a={a}")
        self.a = a
        self.b = b
        self.a_inv = mod_inverse(a, ALPHABET_SIZE)

    def encrypt(self, plaintext):
        result = ""
        for c in plaintext.upper():
            if c in TURKISH_ALPHABET:
                idx = (self.a * TURKISH_ALPHABET.index(c) + self.b) % ALPHABET_SIZE
                result += TURKISH_ALPHABET[idx]
            else:
                result += c
        return result

    def decrypt(self, ciphertext):
        result = ""
        for c in ciphertext.upper():
            if c in TURKISH_ALPHABET:
                idx = (self.a_inv * (TURKISH_ALPHABET.index(c) - self.b)) % ALPHABET_SIZE
                result += TURKISH_ALPHABET[idx]
            else:
                result += c
        return result

class VigenereCipherTR:
    def __init__(self, key):
        self.key = key.upper()

    def encrypt(self, plaintext):
        result = ""
        key_indices = [TURKISH_ALPHABET.index(k) for k in self.key if k in TURKISH_ALPHABET]
        key_len = len(key_indices)
        j = 0
        for c in plaintext.upper():
            if c in TURKISH_ALPHABET:
                idx = (TURKISH_ALPHABET.index(c) + key_indices[j % key_len]) % ALPHABET_SIZE
                result += TURKISH_ALPHABET[idx]
                j += 1
            else:
                result += c
        return result

    def decrypt(self, ciphertext):
        result = ""
        key_indices = [TURKISH_ALPHABET.index(k) for k in self.key if k in TURKISH_ALPHABET]
        key_len = len(key_indices)
        j = 0
        for c in ciphertext.upper():
            if c in TURKISH_ALPHABET:
                idx = (TURKISH_ALPHABET.index(c) - key_indices[j % key_len]) % ALPHABET_SIZE
                result += TURKISH_ALPHABET[idx]
                j += 1
            else:
                result += c
        return result

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
            if algo == "Caesar":
                key1 = int(self.key1_entry.get())
                cipher = CaesarCipherTR(key1)
                result = cipher.encrypt(text)
            elif algo == "Affine":
                key1 = int(self.key1_entry.get())
                key2 = int(self.key2_entry.get())
                cipher = AffineCipherTR(key1, key2)
                result = cipher.encrypt(text)
            elif algo == "Vigenere":
                key1 = self.key1_entry.get()
                cipher = VigenereCipherTR(key1)
                result = cipher.encrypt(text)
            else:
                result = "Algoritma seçilmedi!"
        except Exception as e:
            result = f"Hata: {e}"
        self.result_label.config(text=result)

    def decrypt_text(self):
        text = self.input_text.get()
        algo = self.algorithm.get()
        try:
            if algo == "Caesar":
                key1 = int(self.key1_entry.get())
                cipher = CaesarCipherTR(key1)
                result = cipher.decrypt(text)
            elif algo == "Affine":
                key1 = int(self.key1_entry.get())
                key2 = int(self.key2_entry.get())
                cipher = AffineCipherTR(key1, key2)
                result = cipher.decrypt(text)
            elif algo == "Vigenere":
                key1 = self.key1_entry.get()
                cipher = VigenereCipherTR(key1)
                result = cipher.decrypt(text)
            else:
                result = "Algoritma seçilmedi!"
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
