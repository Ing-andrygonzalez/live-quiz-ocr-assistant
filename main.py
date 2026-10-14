import os
import tkinter as tk
import mss
import pytesseract
from PIL import Image
from openai import OpenAI

# Inicializar cliente de OpenAI (asegúrate de tener tu API key configurada en las variables de entorno de Linux)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class QuizOverlay:

    def __init__(self, root):
        self.root = root
        self.root.title("Live Quiz AI Overlay")

        # Configuración de ventana flotante lateral (pequeña y siempre arriba)
        # Dimensiones: 300x180, posicionada en una esquina de la pantalla
        self.root.geometry("300x180+20+50")
        self.root.wm_attributes("-topmost", True)
        self.root.config(bg="#0b0e11")  # Estilo oscuro profesional

        # Título del panel
        self.lbl_header = tk.Label(
            root,
            text="🤖 LIVE QUIZ ASSISTANT",
            font=("Arial", 10, "bold"),
            fg="#f0b90b",
            bg="#0b0e11",
        )
        self.lbl_header.pack(pady=5)

        # Campo donde saldrá la respuesta ganadora en grande
        self.lbl_result = tk.Label(
            root,
            text="ESPERANDO PREGUNTA...",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#181a20",
            wraplength=280,
            justify="center",
            relief="solid",
            bd=1,
        )
        self.lbl_result.pack(pady=5, padx=10, fill="both", expand=True)

        # Botón de disparo rápido
        self.btn_solve = tk.Button(
            root,
            text="⚡ RESOLVER PANTALLA",
            font=("Arial", 10, "bold"),
            bg="#f0b90b",
            fg="#000000",
            command=self.analyze_quiz,
        )
        self.btn_solve.pack(pady=8)

    def analyze_quiz(self):
        self.lbl_result.config(text="Leyendo y pensando...", fg="#f0b90b")
        self.root.update()

        try:
            # 1. Capturar el área de la pantalla donde tienes el navegador con las preguntas
            with mss.mss() as sct:
                # Coordenadas ajustables según donde ubiques tu ventana en el Chromebook
                monitor = {"top": 100, "left": 100, "width": 800, "height": 600}
                screenshot = sct.grab(monitor)
                img = Image.frombytes(
                    "RGB", screenshot.size, screenshot.bgra, "raw", "BGRX"
                )

            # 2. Extraer texto con OCR
            extracted_text = pytesseract.image_to_string(img, lang="eng")

            if not extracted_text.strip():
                self.lbl_result.config(
                    text="No se detectó texto en la zona", fg="#ed4b9e"
                )
                return

            # 3. Prompt optimizado para la IA (Devuelve el color/forma y la opción correcta)
            prompt = f"""
            You are a hyper-fast quiz solver for live trivia events.
            Analyze the following text extracted from the game. Identify the question and the correct option (Red triangle, Blue diamond, Yellow circle, or Green square).
            
            Extracted text:
            {extracted_text}

            Respond strictly in this concise format (Spanish):
            [Color/Figura] - [Texto corto de la respuesta]
            Example: 🔺 Rojo - Your seed phrase
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=40,
                temperature=0.1,
            )

            answer = response.choices[0].message.content.strip()

            # 4. Mostrar respuesta ganadora en el overlay lateral
            self.lbl_result.config(text=answer, fg="#0ecb81")

        except Exception as e:
            self.lbl_result.config(
                text=f"Error: {str(e)[:30]}...", fg="#ed4b9e"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizOverlay(root)
    root.mainloop()
