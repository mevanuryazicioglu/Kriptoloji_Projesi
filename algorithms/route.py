from algorithms.alphabet import TURKISH_ALPHABET, ALPHABET_SIZE
import math


class RouteCipherTR:
    def __init__(self, cols=4):
        self.cols = cols
        self.alphabet = TURKISH_ALPHABET
        self.m = ALPHABET_SIZE  

    def _create_matrix(self, text):
        text = text.replace(" ", "").upper()
        rows = math.ceil(len(text) / self.cols)
        matrix = []

        idx = 0
        for _ in range(rows):
            row = []
            for _ in range(self.cols):
                if idx < len(text):
                    row.append(text[idx])
                    idx += 1
                else:
                    row.append("X")  
            matrix.append(row)
        return matrix

    def encrypt(self, text):
        matrix = self._create_matrix(text)
        result = ""

        for c in range(self.cols):
            for r in range(len(matrix)):
                result += matrix[r][c]

        return result

    def decrypt(self, text):
        text = text.replace(" ", "").upper()
        rows = math.ceil(len(text) / self.cols)
        matrix = [["" for _ in range(self.cols)] for _ in range(rows)]

        idx = 0
        for c in range(self.cols):
            for r in range(rows):
                if idx < len(text):
                    matrix[r][c] = text[idx]
                    idx += 1

        result = ""
        for r in range(rows):
            for c in range(self.cols):
                result += matrix[r][c]

        return result
