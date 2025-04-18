"""
translate.py
This script translates a DOCX file using the DeepL API.
It reads the file, sends it to the DeepL API for translation, and saves the translated file.
"""
import time
import requests


def translate_file(api_key, api_url, target_lang, source_lang, file_name):
    """
    Translates a DOCX file using the DeepL API.
    Args:
        api_key (str): Your DeepL API key.
        api_url (str): The DeepL API URL.
        target_lang (str): The target language for translation.
        source_lang (str): The source language of the document.
        file_name (str): The name of the DOCX file to be translated.
    """
    with open(file_name, "rb") as file:
        docx_binary = file.read()
        headers = {
            "Authorization": f"DeepL-Auth-Key {api_key}",
        }
        body = {
            "source_lang": source_lang,
            "target_lang": target_lang,
        }
        files = {
            "file": (file_name, docx_binary),
        }
    response = requests.post(api_url, headers=headers,
                             data=body, files=files, timeout=60)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    document_id = response.json().get("document_id")
    document_key = response.json().get("document_key")

    # Wait for the translation to finish
    url = f"{api_url}/{document_id}"
    body = {
        "document_key": document_key,
    }
    response = requests.post(url, headers=headers, data=body, timeout=60)
    response_data = response.json()
    while response_data.get("status") == "translating":
        print("Waiting for translation to finish...")
        time.sleep(response_data.get("seconds_remaining", 5))
        response = requests.post(url, headers=headers, data=body, timeout=60)
        response_data = response.json()

    if response.json().get("status") != "done":
        print("Error: Translation failed")
        print(response.text)
        return

    # Download the translated file
    response = requests.post(
        f"{api_url}/{document_id}/result", headers=headers, data=body, timeout=60)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    with open("translated_file.docx", "wb") as translated_file:
        translated_file.write(response.content)
    print("Translation completed successfully. Translated file saved as 'translated_file.docx'.")
