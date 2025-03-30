from pyrogram import Client, filters
import requests
import os
import base64
from EsproMusic import app

# GitHub credentials
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
GITHUB_REPO = "EsproMusic/cookies"
FILE_NAME = "example.txt"

# Owner ID (Replace with your Telegram user ID)
OWNER_ID = 7946657662  

def is_owner(user_id):
    return user_id == OWNER_ID

@app.on_message(filters.command("add") & filters.private)
async def ask_for_file(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    await message.reply_text("📂 Please send the `cookies.txt` file to upload to GitHub.")

@app.on_message(filters.document & filters.private)
async def upload_to_github(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text("❌ You are not authorized to upload files.")
        return

    if message.document.file_name != FILE_NAME:
        await message.reply_text("❌ Only `cookies.txt` file is allowed! Please send the correct file.")
        return

    file_path = await message.download()

    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode()

    # Get SHA of existing file (required for updating)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_NAME}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    sha = None
    if response.status_code == 200:
        sha = response.json().get("sha")  # Get file SHA if it exists

    # Prepare upload data
    data = {
        "message": "Updated cookies.txt",
        "content": content,
        "sha": sha  # If file exists, SHA is required
    }

    # Upload or update file
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        await message.reply_text(f"✅ `cookies.txt` successfully uploaded to GitHub!\n🔗 [View File](https://github.com/{GITHUB_REPO}/blob/main/{FILE_NAME})")
    else:
        await message.reply_text(f"❌ Upload failed. Error: {response.text}")

    os.remove(file_path)  # Remove file after upload

