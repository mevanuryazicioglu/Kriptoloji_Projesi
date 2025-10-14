class RailFenceCipherTR:
    def __init__(self, rails=3):
        self.rails = rails

    def encrypt(self, text):
        text = text.replace(" ", "").upper()  # Boşlukları kaldır, büyük harf yap
        fence = [[] for _ in range(self.rails)]  # Her ray için boş liste oluştur

        rail = 0  # Başlangıçta ilk raya yazılır
        direction = 1  # 1 = aşağı, -1 = yukarı

        for char in text:
            fence[rail].append(char)

            # Eğer en alt raya geldiysek yönü yukarı çevir
            if rail == self.rails - 1:
                direction = -1
            # Eğer en üst raya geldiysek yönü aşağı çevir
            elif rail == 0:
                direction = 1

            # Yön doğrultusunda bir sonraki raya geç
            rail += direction

        # Tüm rayları birleştirerek şifreli metni oluştur
        result = "".join("".join(row) for row in fence)
        return result

    def decrypt(self, text):
        text = text.replace(" ", "").upper()
        # Zigzag modelini belirlemek için boşluk matrisi oluştur
        pattern = [['' for _ in range(len(text))] for _ in range(self.rails)]

        # Zigzag desenini doldur
        rail = 0
        direction = 1
        for i in range(len(text)):
            pattern[rail][i] = '*'
            if rail == self.rails - 1:
                direction = -1
            elif rail == 0:
                direction = 1
            rail += direction

        # Yıldızların olduğu yerlere sırayla harfleri yerleştir
        index = 0
        for r in range(self.rails):
            for c in range(len(text)):
                if pattern[r][c] == '*' and index < len(text):
                    pattern[r][c] = text[index]
                    index += 1

        # Zigzag sırayla okunarak çözülmüş metin oluşturulur
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