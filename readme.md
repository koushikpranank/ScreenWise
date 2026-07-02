# 🧠 ScreenWise  
### *Turn any on‑screen question into an instant AI‑powered answer*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Selenium](https://img.shields.io/badge/Selenium-4.x-brightgreen) ![Gemini](https://img.shields.io/badge/Gemini-API-orange) ![OCR](https://img.shields.io/badge/Tesseract-OCR-lightgrey)

---

## ✨ What is this?

**ScreenWise** is a playful experiment that combines **browser automation**, **optical character recognition (OCR)**, and **Google’s Gemini AI** to automatically answer multiple‑choice questions you see on any webpage.

Just launch the script, point it to a URL, and every time you press `Enter`, it:
1. Takes a **screenshot** of the current browser view.
2. Runs **OCR** (Tesseract) to extract all visible text.
3. Sends the raw text to **Gemini** with a smart prompt that extracts the question and options, then returns only the correct answer.

> 🤖 **The result?** You get the answer to any on‑screen quiz, survey, or test – instantly!

---

## 🚀 Features

- **One‑click Chrome launch** – starts Chrome with remote debugging (supports Windows & macOS).
- **Intelligent screenshot capture** – grabs exactly what you see in the viewport.
- **Robust OCR** – uses Tesseract, fine‑tuned for screen text.
- **Gemini AI magic** – asks the model to strip away noise and output *only* the correct option.
- **Clean, interactive CLI** – press `Enter` to capture, type `stop` to exit.
- **Automatic cleanup** – closes Chrome even if the script crashes or you hit `Ctrl+C`.

---

## 🧪 Why this is a “fun experiment”

This project is not meant to cheat on exams or violate any rules. Instead, it’s a **demonstration** of how easily you can glue together modern tools:
- Browser automation (Selenium)
- Image‑to‑text extraction (Tesseract)
- Large Language Models (Gemini)

It shows how AI can “read” the screen like a human and answer questions – a small step towards more accessible and interactive web assistants.

---

## 📦 Requirements

- **Python 3.8+**
- **Google Chrome** (installed in default location)
- **Tesseract OCR** ([installation guide](https://github.com/tesseract-ocr/tesseract))
- **Gemini API key** (get one free from [Google AI Studio](https://aistudio.google.com/))

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ScreenWise.git
   cd ScreenWise