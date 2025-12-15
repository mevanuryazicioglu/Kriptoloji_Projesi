# algorithms/rsa.py
import random


class RSACipherTR:
   

    def __init__(self, key_size=512):
        self.key_size = key_size
        self.p = self._generate_prime(key_size // 2)
        self.q = self._generate_prime(key_size // 2)
        # ensure p != q
        while self.q == self.p:
            self.q = self._generate_prime(key_size // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 65537
        # ensure e and phi are coprime
        if self._gcd(self.e, self.phi) != 1:
            # fallback small e
            self.e = 3
        self.d = self._modinv(self.e, self.phi)

        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    # ---------- yardımcı fonksiyonlar ----------
    def _power(self, a, b, n):
        res = 1
        a %= n
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % n
            a = (a * a) % n
            b //= 2
        return res

    def _miller_rabin_test(self, n, k=40):
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            a = random.randint(2, n - 2)
            x = self._power(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = self._power(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def _generate_prime(self, bits):
        while True:
            p = random.getrandbits(bits)
            p |= (1 << bits - 1) | 1  # make sure it's odd and has the correct number of bits
            if self._miller_rabin_test(p):
                return p


    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def _egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self._egcd(b % a, a)
        return (g, x - (b // a) * y, y)

    def _modinv(self, a, m):
        g, x, y = self._egcd(a, m)
        if g != 1:
            raise Exception("Mod inverse yok (a ve m aralarında asal değil).")
        return x % m

    # ---------- şifreleme / deşifreleme ----------
    def encrypt(self, plaintext):
        """
        Her karakteri ayrı ayrı şifreler ve hex string döner (bloklar arası boşluk).
        Örnek çıktı: '7f3a 1b2c ...'
        """
        blocks = []
        for ch in plaintext:
            m = ord(ch)
            c = pow(m, self.e, self.n)
            blocks.append(format(c, 'x'))
        return ' '.join(blocks)

    def decrypt(self, ciphertext_hex):
        """
        ciphertext_hex: hex blokları boşlukla ayrılmış string
        """
        parts = ciphertext_hex.strip().split()
        out = []
        for p in parts:
            if p == '':
                continue
            c = int(p, 16)
            m = pow(c, self.d, self.n)
            out.append(chr(m))
        return ''.join(out)

    # isteğe bağlı: string olarak export/import
    def export_public(self):
        return {"e": self.e, "n": self.n}

    def export_private(self):
        return {"d": self.d, "n": self.n}

    @classmethod
    def from_keys(cls, key_components):
        # key_components: {"e": <int>, "n": <int>} (public) veya {"d": <int>, "n": <int>} (private)
        instance = cls.__new__(cls) # __init__ metodunu çağırmadan yeni bir instance oluştur
        if "d" in key_components:
            instance.d = key_components["d"]
            instance.e = None # Deşifreleme için e gerekli değil
        elif "e" in key_components:
            instance.e = key_components["e"]
            instance.d = None # Şifreleme için d gerekli değil
        else:
            raise ValueError("Geçersiz anahtar bileşenleri. 'd' veya 'e' ve 'n' içermeli.")
        instance.n = key_components["n"]
        # Diğer gerekli alanları (p, q, phi) deşifreleme/şifreleme için ayarlamaya gerek yok
        # eğer sadece d, n veya e, n ile işlem yapılacaksa
        return instance
