import csv
import time
from deep_translator import GoogleTranslator

def translate_idioms():
    translator = GoogleTranslator(source='zh-CN', target='en')
    idioms = []
    
    # Read the existing CSV
    print("Reading idioms from CSV...")
    with open('chinese_idioms.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            idioms.append(row)
    
    # Translate each idiom's meaning
    print("Translating meanings...")
    for idiom in idioms:
        try:
            # Add a small delay to avoid hitting rate limits
            time.sleep(0.5)
            translation = translator.translate(idiom['meaning'])
            idiom['translation'] = translation
            print(f"Translated: {idiom['chinese']} - {translation}")
        except Exception as e:
            print(f"Translation error for '{idiom['chinese']}': {e}")
            idiom['translation'] = None
    
    # Save to a new CSV with translations
    print("Saving translations to CSV...")
    with open('chinese_idioms_with_translations.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chinese', 'pinyin', 'meaning', 'translation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idiom in idioms:
            writer.writerow(idiom)
    
    print("Translation complete! Results saved to chinese_idioms_with_translations.csv")

if __name__ == "__main__":
    translate_idioms() 