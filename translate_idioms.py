import csv
import time
from deep_translator import GoogleTranslator

def read_idioms_from_csv(filename='chinese_idioms.csv'):
    """Read idioms from a CSV file."""
    idioms = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            idioms.append(row)
    return idioms

def translate_meaning(translator, meaning):
    """Translate a single meaning with error handling."""
    try:
        # Add a small delay to avoid hitting rate limits
        time.sleep(0.5)
        return translator.translate(meaning)
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def translate_idioms_list(translator, idioms):
    """Translate meanings for a list of idioms."""
    for idiom in idioms:
        translation = translate_meaning(translator, idiom['meaning'])
        idiom['translation'] = translation
        if translation:
            print(f"Translated: {idiom['chinese']} - {translation}")
        else:
            print(f"Failed to translate: {idiom['chinese']}")

def save_translations_to_csv(idioms, filename='chinese_idioms_with_translations.csv'):
    """Save idioms with translations to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chinese', 'pinyin', 'meaning', 'translation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idiom in idioms:
            writer.writerow(idiom)
    print(f"Translation complete! Results saved to {filename}")

def translate_idioms():
    """Main function to translate idioms."""
    print("Reading idioms from CSV...")
    idioms = read_idioms_from_csv()
    
    print("Translating meanings...")
    translator = GoogleTranslator(source='zh-CN', target='en')
    translate_idioms_list(translator, idioms)
    
    print("Saving translations to CSV...")
    save_translations_to_csv(idioms)

if __name__ == "__main__":
    translate_idioms() 