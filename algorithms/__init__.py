class CryptoGUI:
    def __init__(self):
        try:
            self.client = Client()
            self.window = tk.Tk()
            self.window.title("Kriptoloji Projesi")
            self.window.geometry("450x400")
            print("Tkinter penceresi oluşturuldu")
        except Exception as e:
            print("GUI oluşturulurken hata:", e)
