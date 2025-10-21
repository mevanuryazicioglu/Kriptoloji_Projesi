from algorithms.alphabet import TURKISH_ALPHABET

class ColumnarCipherTR:
    def __init__(self, key=None):
        self.key = key  # Anahtar kelime (örneğin "KOD")
        self.alphabet = TURKISH_ALPHABET

    def _order_key(self):
        """Anahtardaki harflerin alfabetik sırasını döndürür."""
        return sorted(range(len(self.key)), key=lambda k: self.key[k])

    def encrypt(self, text):
        if not self.key:
            raise ValueError("Anahtar (key) belirtilmeli.")

        text = text.upper().replace(" ", "")
        columns = len(self.key)
        key_order = self._order_key()

        rows = [text[i:i + columns] for i in range(0, len(text), columns)]

        if len(rows[-1]) < columns:
            rows[-1] += "X" * (columns - len(rows[-1]))

        cipher_text = ""
        for col in key_order:
            for row in rows:
                cipher_text += row[col]
        return cipher_text

    def decrypt(self, text):
        if not self.key:
            raise ValueError("Anahtar (key) belirtilmeli.")

        text = text.upper().replace(" ", "")
        columns = len(self.key)
        key_order = self._order_key()

        rows = len(text) // columns

        matrix = [[""] * columns for _ in range(rows)]

        idx = 0
        for col in key_order:
            for row in range(rows):
                matrix[row][col] = text[idx]
                idx += 1

        plain_text = "".join("".join(row) for row in matrix)
        return plain_text.rstrip("X")
