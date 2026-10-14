import os
import tkinter as tk
import mss
import pytesseract
from PIL import Image
from google import genai

# Inicializar cliente de Google Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class QuizOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Quiz AI Overlay")

        # Configuración de ventana flotante (pequeña y siempre arriba)
        self.root.geometry("320x200+20+50")
        self.root.wm_attributes("-topmost", True)
        self.root.config(bg="#0b0e11")

        # Título
        self.title_label = tk.Label(
            root, text="⚡ Quiz Assistant (Gemini)", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#0b0e11"
        )
        self.title_label.pack(pady=5)

        # Botón para capturar y resolver
        self.solve_btn = tk.Button(
            root, text="⚡ RESOLVER PANTALLA", font=("Arial", 10, "bold"),
            bg="#1f6feb", fg="white", activebackground="#388bfd",
            command=self.process_screen
        )
        self.solve_btn.pack(pady=5, fill="x", padx=15)

        # Área de respuesta
        self.result_label = tk.Label(
            root, text="Esperando captura...", font=("Arial", 10),
            fg="#e6edf3", bg="#161b22", wraplength=280, justify="left",
            relief="solid", bd=1
        )
        self.result_label.pack(pady=5, fill="both", expand=True, padx=10)

    def process_screen(self):
        self.result_label.config(text="🔍 Leyendo pantalla y analizando...")
        self.root.update() 

        try:
            # Captura de TODA la pantalla en lugar de una región limitada
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # OCR: Extraer texto con Tesseract
            text = pytesseract.image_to_string(img, lang="spa+eng").strip()

            if not text or len(text) < 5:
                self.result_label.config(text="❌ No se detectó texto claro.")
                return

            # Consulta a la IA de Gemini
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