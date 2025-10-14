class RailFenceCipherTR:
    def __init__(self, rails=3):
        self.rails = rails

    def encrypt(self, text):
        text = text.replace(" ", "").upper()  
        fence = [[] for _ in range(self.rails)]  

        rail = 0  
        direction = 1  

        for char in text:
            fence[rail].append(char)

            if rail == self.rails - 1:
                direction = -1
            elif rail == 0:
                direction = 1

            rail += direction

        result = "".join("".join(row) for row in fence)
        return result

    def decrypt(self, text):
        text = text.replace(" ", "").upper()
        pattern = [['' for _ in range(len(text))] for _ in range(self.rails)]

        rail = 0
        direction = 1
        for i in range(len(text)):
            pattern[rail][i] = '*'
            if rail == self.rails - 1:
                direction = -1
            elif rail == 0:
                direction = 1
            rail += direction

        index = 0
        for r in range(self.rails):
            for c in range(len(text)):
                if pattern[r][c] == '*' and index < len(text):
                    pattern[r][c] = text[index]
                    index += 1

        result = ""
        rail = 0
        direction = 1
        for c in range(len(text)):
            result += pattern[rail][c]
            if rail == self.rails - 1:
                direction = -1
            elif rail == 0:
                direction = 1
            rail += direction

        return result