from algorithms.alphabet import TURKISH_ALPHABET

class PolybiusCipherTR:
    def __init__(self):
        self.alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
        self.rows = 6
        self.cols = 5

    def _create_grid(self):
        grid = []
        idx = 0
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if idx < len(self.alphabet):
                    row.append(self.alphabet[idx])
                    idx += 1
                else:
                    row.append("X")
            grid.append(row)
        return grid

    def encrypt(self, text):
        text = text.upper().replace(" ", "")
        grid = self._create_grid()
        result = ""
        for char in text:
            found = False
            for r, row in enumerate(grid):
                if char in row:
                    c = row.index(char)
                    result += f"{r+1}{c+1}"
                    found = True
                    break
            if not found:
                result += char  
        return result

    def decrypt(self, text):
        grid = self._create_grid()
        result = ""
        i = 0
        while i < len(text):
            if text[i].isdigit() and i + 1 < len(text) and text[i + 1].isdigit():
                r = int(text[i]) - 1
                c = int(text[i + 1]) - 1
                if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
                    result += grid[r][c]
                else:
                    result += "?"
                i += 2
            else:
                result += text[i]
                i += 1
        return result
