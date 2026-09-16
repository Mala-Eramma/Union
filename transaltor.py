import urllib.request
import urllib.parse
import json

# Get user input
source_lang = input("Enter source language code (e.g. en, hi, te): ")
destination_lang = input("Enter destination language code (e.g. en, hi, te): ")
text = input("Enter text to translate: ")

# Build URL
url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode({
    "client": "gtx",
    "sl": source_lang,
    "tl": destination_lang,
    "dt": "t",
    "q": text
})

# Translate
with urllib.request.urlopen(url) as response:
    result = json.loads(response.read().decode("utf-8"))

translated_text = "".join(part[0] for part in result[0])

print("\nTranslated Text:")
print(translated_text)