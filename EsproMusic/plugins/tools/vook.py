from pyrogram import Client, filters
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from EsproMusic import app


def get_youtube_cookies():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://www.youtube.com")
    time.sleep(5)  # Wait for page to load
    
    cookies = driver.get_cookies()
    driver.quit()
    
    cookies_text = "\n".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    with open("example.txt", "w") as f:
        f.write(cookies_text)
    
    return "example.txt"

@app.on_message(filters.command("generate"))
def generate_cookies(client, message):
    message.reply_text("Generating YouTube cookies, please wait...")
    file_path = get_youtube_cookies()
    message.reply_document(file_path)

