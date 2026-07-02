# 🧠 ScreenWise

### _Turn any on‑screen question into an instant AI‑powered answer_

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
- **Gemini AI magic** – asks the model to strip away noise and output _only_ the correct option.
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

   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   _(Create a `requirements.txt` with:)_

   ```
   pytesseract
   pillow
   selenium
   requests
   ```

3. **Set up Tesseract** (if not in PATH)
   - On macOS: `brew install tesseract`
   - On Windows: download and install from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - On Linux: `sudo apt install tesseract-ocr`

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://aistudio.google.com/), create an API key.
   - Replace the placeholder in the script:
     ```python
     GEMINI_API_KEY = "YOUR_ACTUAL_KEY"
     ```
   - Or better, use an environment variable for security.

---

## ▶️ Usage

Run the script from your terminal:

```bash
python screenwise.py
```

The script will:

- Launch Chrome automatically.
- Ask for a URL.
- Navigate to that page (you can also manually browse afterwards).
- Enter an interactive loop:
  - Press `Enter` → capture, OCR, ask Gemini, and print the answer.
  - Type `stop` → exit and close Chrome.

---

## 🧠 How it works (under the hood)

1. **Launch & connect**  
   `subprocess` starts Chrome with `--remote-debugging-port`, then Selenium attaches to that instance.

2. **Screenshot & OCR**  
   `driver.save_screenshot()` captures the viewport; `pytesseract` extracts text.

3. **Gemini prompt**  
   We craft a strict prompt that tells Gemini to:
   - Ignore headers, timestamps, and clutter.
   - Identify the question and options.
   - Output _only_ the correct option text – no explanations, no extra words.

4. **Cleanup**  
   `atexit` and signal handlers ensure Chrome is terminated, even if you interrupt the script.

---

## 📸 Demo

```plaintext
$ python screenwise.py
2025-03-24 10:15:32 - INFO - Launching Chrome with command: ...
Enter the URL to navigate to: https://example.com/quiz
2025-03-24 10:15:45 - INFO - Page loaded. You can now navigate manually.

Enter command (press Enter to capture, or type 'stop' to quit):
2025-03-24 10:16:01 - INFO - Capturing screenshot...
2025-03-24 10:16:01 - INFO - Running OCR...
2025-03-24 10:16:03 - INFO - Sending raw OCR text to Gemini...

============================================================
RAW OCR TEXT (first 300 chars):
Which planet is known as the Red Planet?
A) Venus
B) Mars
C) Jupiter
D) Saturn
...
------------------------------------------------------------
Gemini's answer: B) Mars
============================================================
```

---

## ⚠️ Important Notes

- **Ethical use**: This tool is meant for **educational and experimental purposes only**. Respect website terms of service. Do not use it to cheat on exams or circumvent any restrictions.
- **Accuracy**: OCR quality depends on the page font and layout. Gemini’s answer is only as good as the extracted text.
- **API costs**: Gemini API calls are not free after the initial free tier – monitor your usage.

---

## 🔧 Future improvements

- Support for **headless mode** and **stealth** to avoid detection.
- Add **GUI** for easier interaction.
- **Save history** of captures and answers.
- **Multi‑language** OCR support.

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! Feel free to fork and experiment – this is a playground project, so have fun with it.

---

## 📄 License

MIT – see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Selenium](https://www.selenium.dev/)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- The open‑source community for all the amazing tools that make experiments like this possible.

---

**Made with 💡 curiosity and ☕ coffee.**

```

---

### 🎯 Tips for your GitHub repo

- Add a **demo GIF** showing the script in action.
- Include the `requirements.txt` file.
- Keep the API key out of the code – use environment variables (mention that in the README).
- Add a clear license (e.g., MIT).

This README balances technical details with an engaging narrative, making it perfect for a fun, educational experiment on GitHub.
```
# 🧠 ScreenWise

### _Turn any on‑screen question into an instant AI‑powered answer_

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
- **Gemini AI magic** – asks the model to strip away noise and output _only_ the correct option.
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

   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   _(Create a `requirements.txt` with:)_

   ```
   pytesseract
   pillow
   selenium
   requests
   ```

3. **Set up Tesseract** (if not in PATH)
   - On macOS: `brew install tesseract`
   - On Windows: download and install from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - On Linux: `sudo apt install tesseract-ocr`

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://aistudio.google.com/), create an API key.
   - Replace the placeholder in the script:
     ```python
     GEMINI_API_KEY = "YOUR_ACTUAL_KEY"
     ```
   - Or better, use an environment variable for security.

---

## ▶️ Usage

Run the script from your terminal:

```bash
python screenwise.py
```

The script will:

- Launch Chrome automatically.
- Ask for a URL.
- Navigate to that page (you can also manually browse afterwards).
- Enter an interactive loop:
  - Press `Enter` → capture, OCR, ask Gemini, and print the answer.
  - Type `stop` → exit and close Chrome.

---

## 🧠 How it works (under the hood)

1. **Launch & connect**  
   `subprocess` starts Chrome with `--remote-debugging-port`, then Selenium attaches to that instance.

2. **Screenshot & OCR**  
   `driver.save_screenshot()` captures the viewport; `pytesseract` extracts text.

3. **Gemini prompt**  
   We craft a strict prompt that tells Gemini to:
   - Ignore headers, timestamps, and clutter.
   - Identify the question and options.
   - Output _only_ the correct option text – no explanations, no extra words.

4. **Cleanup**  
   `atexit` and signal handlers ensure Chrome is terminated, even if you interrupt the script.

---

## 📸 Demo

```plaintext
$ python screenwise.py
2025-03-24 10:15:32 - INFO - Launching Chrome with command: ...
Enter the URL to navigate to: https://example.com/quiz
2025-03-24 10:15:45 - INFO - Page loaded. You can now navigate manually.

Enter command (press Enter to capture, or type 'stop' to quit):
2025-03-24 10:16:01 - INFO - Capturing screenshot...
2025-03-24 10:16:01 - INFO - Running OCR...
2025-03-24 10:16:03 - INFO - Sending raw OCR text to Gemini...

============================================================
RAW OCR TEXT (first 300 chars):
Which planet is known as the Red Planet?
A) Venus
B) Mars
C) Jupiter
D) Saturn
...
------------------------------------------------------------
Gemini's answer: B) Mars
============================================================
```

---

## ⚠️ Important Notes

- **Ethical use**: This tool is meant for **educational and experimental purposes only**. Respect website terms of service. Do not use it to cheat on exams or circumvent any restrictions.
- **Accuracy**: OCR quality depends on the page font and layout. Gemini’s answer is only as good as the extracted text.
- **API costs**: Gemini API calls are not free after the initial free tier – monitor your usage.

---

## 🔧 Future improvements

- Support for **headless mode** and **stealth** to avoid detection.
- Add **GUI** for easier interaction.
- **Save history** of captures and answers.
- **Multi‑language** OCR support.

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! Feel free to fork and experiment – this is a playground project, so have fun with it.

---

## 📄 License

MIT – see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Selenium](https://www.selenium.dev/)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- The open‑source community for all the amazing tools that make experiments like this possible.

---

**Made with 💡 curiosity and ☕ coffee.**

```

---

### 🎯 Tips for your GitHub repo

- Add a **demo GIF** showing the script in action.
- Include the `requirements.txt` file.
- Keep the API key out of the code – use environment variables (mention that in the README).
- Add a clear license (e.g., MIT).

This README balances technical details with an engaging narrative, making it perfect for a fun, educational experiment on GitHub.
```
