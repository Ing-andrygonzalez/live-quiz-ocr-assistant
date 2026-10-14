import os
import tkinter as tk
import pytesseract
from PIL import Image
from google import genai

# Inicializar cliente de Google Gemini
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
        self.result_label.config(text="🔍 Capturando y analizando...")
        self.root.update()

        try:
            # Tomar captura de pantalla con scrot
            os.system("scrot -f /tmp/screen_capture.png")
            img = Image.open("/tmp/screen_capture.png")

            # OCR: Extraer texto
            text = pytesseract.image_to_string(img, lang="eng+spa").strip()

            if not text or len(text) < 3:
                self.result_label.config(text="❌ No se detectó texto claro.")
                return

            # Consulta a Gemini
            prompt = f"Analiza esta pregunta de trivia u opción múltiple y dame ÚNICAMENTE la respuesta correcta de forma directa y concisa:\n\n{text}"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            answer = response.text.strip()
            self.result_label.config(text=f"💡 {answer}")

        except Exception as e:
            self.result_label.config(text=f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizOverlay(root)
    root.mainloop()