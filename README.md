# docx-translator

Python script to translate a docx into a specified language using the DEEPL Document Translation API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## How to use:

1. Place the `.exe` and the `.env` file in the same directory as your docx file.
1. Open the `.env` file and enter your set your environment values (see [Environment Variables](#environment-variables)).
1. Run the EXE and wait for the translation to finish. (This might take a while)
1. Enjoy your translated document

## Environment Variables

| KEY             | VALUE                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| SOURCE_LANGUAGE | The language of the document you want to translate. For example, if you want to translate from English to German, set this to EN. |
| TARGET_LANGUAGE | The language you want to translate to. For example, if you want to translate from English to German, set this to DE.              |
| DEEP_L_API_KEY  | Your DEEPL API key. You can get a free API key from the DEEPL website.                                                            |
| API_URL         | The url to the DEEPL API, e.g. https://api-free.deepl.com/v2/document if you are using the free API.                              |
| FILE_NAME       | The name of the file you want to translate.                                                                                       |

## Contributing

If you want to contribute to this project, feel free to open an issue or a pull request. I will try to respond as soon as possible.
