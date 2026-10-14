import os
import time
import tkinter as tk
import subprocess
from PIL import Image
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
            screenshot_path = "/tmp/screenshot.png"
            subprocess.run(["scrot", "-z", screenshot_path], check=True)

            img = Image.open(screenshot_path)
            img.thumbnail((1024, 1024))

            self.result_label.config(text="⚡ Analizando...")
            self.root.update()

            prompt = "Lee la pregunta de trivia y opciones en la imagen. Responde SOLO con el texto de la opción correcta, de forma súper breve."

            max_retries = 5
            answer = ""
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[img, prompt],
                    )
                    answer = response.text.strip()
                    break
                except Exception as api_err:
                    err_str = str(api_err)
                    if ("503" in err_str or "Unavailable" in err_str) and attempt < max_retries - 1:
                        self.result_label.config(text=f"⚠️ Servidor ocupado, reintentando ({attempt + 1}/{max_retries})...")
                        self.root.update()
                        time.sleep(2.5)
                    else:
                        raise api_err

            self.result_label.config(text=f"💡 {answer}")

        except Exception as e:
            self.result_label.config(text=f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizOverlay(root)
    root.mainloop()
