"""
main.py
This script handles environment variables for the DeepL API translation process.
It serves as the entry point for the translation script.
"""
import os
from dotenv import load_dotenv
from translate import translate_file

if __name__ == "__main__":
    load_dotenv("config.env")
    api_key = os.getenv("DEEP_L_API_KEY")
    api_url = os.getenv("API_URL")
    target_lang = os.getenv("TARGET_LANGUAGE")
    source_lang = os.getenv("SOURCE_LANGUAGE")
    file_name = os.getenv("FILE_NAME")

    translate_file(api_key, api_url, target_lang, source_lang, file_name)
