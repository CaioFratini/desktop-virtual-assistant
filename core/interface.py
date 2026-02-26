import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from core.spotify import _musica_atual

class LainInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The wired")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.width = 800
        self.height = 600
        self.running = True
        self.messages = []
        self.message_count = 0

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.window_frame = tk.Frame(self.root, bg="lightgray", bd=2, relief="raised")
        self.window_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.canvas = tk.Canvas(self.window_frame, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.root.bind("<Configure>", self._on_resize)

        self.scanline_id = None
        self.scanline_tk = None
        self._create_scanlines()
        self._animate_scanlines()

    def _on_resize(self, event):
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self._create_scanlines()
        self._redraw_text()

    def _create_scanlines(self):
        image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        for y in range(0, self.height, 4):
            draw.line((0, y, self.width, y), fill=(0, 255, 0, 25))
        self.scanline_tk = ImageTk.PhotoImage(image)

        if self.scanline_id is None:
            self.scanline_id = self.canvas.create_image(0, 0, anchor="nw", image=self.scanline_tk)
        else:
            self.canvas.itemconfig(self.scanline_id, image=self.scanline_tk)

    def _animate_scanlines(self):
        if not self.running:
            return
        self.canvas.move(self.scanline_id, 0, 1)
        self.root.after(60, self._reverse_scanlines)

    def _reverse_scanlines(self):
        if not self.running:
            return
        self.canvas.move(self.scanline_id, 0, -1)
        self.root.after(60, self._animate_scanlines)

    def mostrar_mensagem(self, mensagem: str):
        self.message_count += 1
        if self.message_count > 15:
            self.messages = [_musica_atual()]
            self.message_count = 1
        else:
            self.messages.append(mensagem)
        self._redraw_text()

    def _redraw_text(self):
        self.canvas.delete("text")
        y = 20
        for msg in self.messages[-25:]:
            self.canvas.create_text(
                10, y,
                anchor="nw",
                text=f"> {msg}",
                fill="#00ff00",
                font=("Courier", 14),
                tags="text"
            )
            y += 20

    def iniciar(self):
        self.root.mainloop()

    def parar(self):
        self.running = False
        self.root.destroy()
