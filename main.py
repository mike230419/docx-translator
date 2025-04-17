import time
import requests
import os

DEEP_L_API_KEY = "REPLACE_DEEP_L_API_KEY"
TARGET_LANGUAGE = "REPLACE_TARGET_LANGUAGE"
SOURCE_LANGUAGE = "REPLACE_SOURCE_LANGUAGE"
FILE_NAME = "REPLACE_FILE_NAME"
API_URL = "REPLACE_API_URL"

def use_env_values_if_available():
    """
    Uses environment variables if available.
    """
    global DEEP_L_API_KEY, TARGET_LANGUAGE, SOURCE_LANGUAGE, FILE_NAME, API_URL
    DEEP_L_API_KEY = os.getenv("DEEP_L_API_KEY", DEEP_L_API_KEY)
    TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", TARGET_LANGUAGE)
    SOURCE_LANGUAGE = os.getenv("SOURCE_LANGUAGE", SOURCE_LANGUAGE)
    FILE_NAME = os.getenv("FILE_NAME", FILE_NAME)
    API_URL = os.getenv("API_URL", API_URL)
    
    print(f"Using API URL: {API_URL}")
    print(f"Using file name: {FILE_NAME}")
    print(f"Using source language: {SOURCE_LANGUAGE}")
    print(f"Using target language: {TARGET_LANGUAGE}")
    print(f"Using DeepL API key: {DEEP_L_API_KEY}")

def translate_file():
    """
    Translates a DOCX file using the DeepL API.
    """
    with open(FILE_NAME, "rb") as file:
        docx_binary = file.read()
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEP_L_API_KEY}",
        }
        body = {
            "source_lang": SOURCE_LANGUAGE,
            "target_lang": TARGET_LANGUAGE,
        }
        files = {
            "file": (FILE_NAME, docx_binary),
        }
    response = requests.post(API_URL, headers=headers, data=body, files=files)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    document_id = response.json().get("document_id")
    document_key = response.json().get("document_key")

    # Wait for the translation to finish
    url = f"{API_URL}/{document_id}"
    body = {
        "document_key": document_key,
    }
    response = requests.post(url, headers=headers, data=body)
    while response.json().get("status") == "translating":
        print("Waiting for translation to finish...")
        time.sleep(response.json().get("seconds_remaining", 5))
        response = requests.post(url, headers=headers, data=body)
    
    if response.json().get("status") != "done":
        print("Error: Translation failed")
        print(response.text)
        return
    
    # Download the translated file
    response = requests.post(f"{API_URL}/{document_id}/result", headers=headers, data=body)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    with open("translated_file.docx", "wb") as translated_file:
        translated_file.write(response.content)
    print("Translation completed successfully. Translated file saved as 'translated_file.docx'.")

if __name__ == "__main__":
    use_env_values_if_available()
    translate_file()
