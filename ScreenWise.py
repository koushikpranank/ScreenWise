import pytesseract
import re
import time
import sys
import logging
import requests
import json
import os
import subprocess
import platform
import atexit
import signal
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ----------------------------------------------------------------------
# LOGGING SETUP
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
REMOTE_DEBUGGING_PORT = 9222          # Must match Chrome's debugging port
TESSERACT_CMD = None                  # Set if Tesseract is not in PATH

if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Gemini API configuration – get key from environment or prompt
GEMINI_API_KEY = "YOUR_ACTUAL_KEY"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

# Global variable to hold the Chrome process
chrome_process = None

# ----------------------------------------------------------------------
# CLEANUP FUNCTION
# ----------------------------------------------------------------------
def cleanup_chrome():
    """Terminate the Chrome process if it's still running."""
    global chrome_process
    if chrome_process is not None:
        try:
            if chrome_process.poll() is None:  # Process is still running
                logger.info("Terminating Chrome process...")
                chrome_process.terminate()
                # Give it a few seconds to shut down gracefully
                time.sleep(2)
                if chrome_process.poll() is None:
                    logger.warning("Chrome did not terminate; forcing kill...")
                    chrome_process.kill()
                logger.info("Chrome process terminated.")
        except Exception as e:
            logger.error("Error during Chrome cleanup: %s", e)
        finally:
            chrome_process = None

# ----------------------------------------------------------------------
# LAUNCH CHROME WITH REMOTE DEBUGGING
# ----------------------------------------------------------------------
def launch_chrome(port=REMOTE_DEBUGGING_PORT):
    """
    Starts Google Chrome with remote debugging enabled on the specified port.
    Detects OS and uses appropriate command.
    Returns the Popen object or None on failure.
    """
    global chrome_process
    system = platform.system()
    if system == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user_data_dir = os.path.expanduser("~/ChromeAutomation")
        cmd = [
            chrome_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}"
        ]
    elif system == "Windows":
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        user_data_dir = r"C:\ChromeAutomation"
        cmd = [
            chrome_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}"
        ]
    else:
        logger.error("Unsupported OS: %s", system)
        return None

    logger.info("Launching Chrome with command: %s", " ".join(cmd))
    try:
        # Start Chrome as a detached process (no wait)
        chrome_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("Chrome launched (PID: %d). Waiting for it to initialize...", chrome_process.pid)
        time.sleep(3)  # Give Chrome time to start
        return chrome_process
    except Exception as e:
        logger.error("Failed to launch Chrome: %s", e)
        return None

# ----------------------------------------------------------------------
# CONNECT TO REMOTE CHROME
# ----------------------------------------------------------------------
def connect_to_chrome(port=REMOTE_DEBUGGING_PORT):
    """
    Connects to an already running Chrome instance with remote debugging enabled.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(options=chrome_options)
    logger.info("Successfully connected to remote Chrome on port %d", port)
    return driver

# ----------------------------------------------------------------------
# CAPTURE & OCR
# ----------------------------------------------------------------------
def capture_screenshot(driver, filename="screenshot.png"):
    """Capture current viewport and return PIL Image."""
    driver.save_screenshot(filename)
    logger.info("Screenshot saved as %s", filename)
    return Image.open(filename)

def ocr_image(image):
    """Perform OCR and return extracted text."""
    try:
        text = pytesseract.image_to_string(image, config='--psm 6')
        logger.info("OCR completed, extracted %d characters", len(text))
        return text
    except Exception as e:
        logger.error("OCR failed: %s", e)
        return ""

# ----------------------------------------------------------------------
# GEMINI API CALL (using raw OCR text)
# ----------------------------------------------------------------------
def query_gemini_raw(raw_text, api_key):
    """
    Send the raw OCR text to Gemini with a prompt asking for a one‑word answer.
    Returns the parsed answer string (or None on failure).
    """
    prompt = f"""
        You are a precise question-answering assistant. Your sole task is to extract the question and options from the raw text provided below, and output ONLY the exact text of the correct option.
        Rules:
        1. Filter out all background noise, timestamps, and UI text from the raw text.
        2. Identify the core question and the multiple-choice options.
        3. Output ONLY the correct option text. 
        4. Do NOT include explanations, conversational filler, introductory text, punctuation, or any extra words.
        Raw Text:
        {raw_text}
        Answer:
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            logger.error("No candidates in Gemini response")
            return None
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            logger.error("No parts in Gemini response")
            return None
        answer = parts[0].get("text", "").strip()
        return answer
    except requests.exceptions.RequestException as e:
        logger.error("Gemini API request failed: %s", e)
        return None

# ----------------------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------------------
def main():
    global chrome_process

    # Register cleanup function to run on normal exit
    atexit.register(cleanup_chrome)

    # Set up signal handler for SIGINT (Ctrl+C) to ensure cleanup
    def signal_handler(sig, frame):
        logger.info("Received interrupt signal. Cleaning up...")
        cleanup_chrome()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 1. Launch Chrome with remote debugging
    if not launch_chrome():
        logger.error("Chrome launch failed. Please start Chrome manually with the correct flags.")
        return

    # 2. Connect to Chrome
    try:
        driver = connect_to_chrome()
    except Exception as e:
        logger.error("Could not connect to Chrome: %s", e)
        logger.error("Make sure Chrome is running with --remote-debugging-port=%d", REMOTE_DEBUGGING_PORT)
        cleanup_chrome()  # Ensure Chrome is terminated if connection failed
        return

    # 3. Ask for URL and navigate
    url = input("Enter the URL to navigate to: ").strip()
    if not url:
        logger.error("No URL provided. Exiting.")
        driver.quit()
        cleanup_chrome()
        return

    try:
        logger.info("Navigating to %s ...", url)
        driver.get(url)
        logger.info("Page loaded. You can now navigate manually in the browser.")
    except Exception as e:
        logger.error("Failed to navigate: %s", e)
        driver.quit()
        cleanup_chrome()
        return

    # 4. Main capture loop
    try:
        while True:
            cmd = input("\nEnter command (press Enter to capture, or type 'stop' to quit): ").strip().lower()
            if cmd == 'stop':
                logger.info("Stop command received. Exiting.")
                break

            # ---- CAPTURE & PROCESS ----
            try:
                logger.info("Capturing screenshot...")
                img = capture_screenshot(driver)

                logger.info("Running OCR...")
                ocr_text = ocr_image(img)
                if not ocr_text:
                    logger.warning("OCR returned empty text. Check if page has readable text.")
                    continue

                # Send raw text to Gemini
                logger.info("Sending raw OCR text to Gemini...")
                gemini_answer = query_gemini_raw(ocr_text, GEMINI_API_KEY)

                # Print results
                print("\n" + "=" * 60)
                print("RAW OCR TEXT (first 300 chars):")
                print(ocr_text[:300] + ("..." if len(ocr_text) > 300 else ""))
                print("-" * 60)
                if gemini_answer:
                    print(f"Gemini's answer: {gemini_answer}")
                else:
                    print("Gemini did not return a valid answer.")
                print("=" * 60)

            except Exception as e:
                logger.error("Error during capture/OCR/Gemini: %s", e, exc_info=True)
                print(f"An error occurred: {e}. Check logs for details.")

    except KeyboardInterrupt:
        logger.info("Interrupted by user (Ctrl+C).")
    finally:
        driver.quit()
        logger.info("Browser session closed.")
        cleanup_chrome()  # Ensure Chrome is terminated even if driver quit didn't

if __name__ == "__main__":
    main()