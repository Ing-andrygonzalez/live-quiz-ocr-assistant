# Live Quiz OCR Assistant 🤖⚡

A lightweight, real-time visual overlay assistant powered by OpenAI (`gpt-4o-mini`) and OCR (Tesseract) to quickly process multiple-choice quiz questions on screen and suggest the correct option in milliseconds.

Designed specifically to assist with high-speed online quizzes and live stream trivia events where reaction time is critical.

---

## 🌟 Key Features

- **On-Screen Overlay UI:** Non-intrusive floating window (`Tkinter`) that stays on top of your browser or application.
- **Instant Screen Capture:** Fast region-based screenshot capture using `mss`.
- **Optical Character Recognition (OCR):** Extracts text directly from the captured region via `pytesseract`.
- **Fast Reasoning Engine:** Leverages OpenAI's ultra-fast `gpt-4o-mini` model to parse options and determine the correct answer instantly.
- **Color/Shape Mapping:** Formatted specifically to highlight options by color, letter, or symbol for frictionless clicking.

---

## 🛠️ Architecture Overview


