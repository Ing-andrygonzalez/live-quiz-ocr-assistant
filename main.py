import os
import tkinter as tk
import pyscreenshot as ImageGrab
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class QuizOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Quiz AI Overlay")

        self.root.geometry("320x220+20+50")
        self.root.wm_attributes("-topmost", True)
        self.root.config(bg="#0b0e11")

        self.title_label = tk.Label(
            root, text="⚡ Quiz Assistant (Gemini)", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#0b0e11"
        )
        self.title_label.pack(pady=5)

        self.solve_btn = tk.Button(
            root, text="⚡ RESOLVER PANTALLA", font=("Arial", 10, "bold"),
            bg="#1f6feb", fg="white", activebackground="#388bfd",
            command=self.process_screen
        )
        self.solve_btn.pack(pady=5, fill="x", padx=15)

        self.result_label = tk.Label(
            root, text="Esperando captura...", font=("Arial", 10),
            fg="#e6edf3", bg="#161b22", wraplength=280, justify="left",
            relief="solid", bd=1
        )
        self.result_label.pack(pady=5, fill="both", expand=True, padx=10)

    def process_screen(self):
        self.result_label.config(text="🔍 Capturando pantalla...")
        self.root.update()

        try:
            # Captura directa en memoria con pyscreenshot
            img = ImageGrab.grab()

            self.result_label.config(text="🔍 Analizando con Gemini...")
            self.root.update()

            # Enviar la imagen a Gemini 2.5 Flash
            prompt = "Lee la pregunta de trivia y las opciones en esta imagen. Responde ÚNICAMENTE con la opción de respuesta correcta, de forma breve y directa."
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
            )

            answer = response.text.strip()
            self.result_label.config(text=f"💡 {answer}")

        except Exception as e:
            self.result_label.config(text=f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizOverlay(root)
    root.mainloop()