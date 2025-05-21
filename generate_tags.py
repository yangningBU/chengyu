import csv
import jieba
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def clean_text(text):
    """Clean text by removing special characters and extra spaces."""
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_chinese_keywords(text):
    """Extract keywords from Chinese text using jieba."""
    # Add custom words that might be important for idioms
    custom_words = ['比喻', '形容', '指', '形容', '比喻']
    for word in custom_words:
        jieba.add_word(word)
    
    words = jieba.cut(text)
    # Filter out single characters and common words
    words = [w for w in words if len(w) > 1 and w not in ['的', '了', '是', '在', '有', '和', '与', '或']]
    return words

def extract_english_keywords(text):
    """Extract keywords from English text using NLTK."""
    # Simple word tokenization without sentence splitting
    words = text.lower().split()
    # Remove stopwords and short words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words and len(w) > 2]
    return words

def generate_tags(chinese_meaning, english_meaning):
    """Generate tags based on both Chinese and English meanings."""
    # Clean the texts
    chinese_meaning = clean_text(chinese_meaning)
    english_meaning = clean_text(english_meaning)
    
    # Extract keywords from both languages
    chinese_keywords = extract_chinese_keywords(chinese_meaning)
    english_keywords = extract_english_keywords(english_meaning)
    
    # Combine and count keywords
    all_keywords = chinese_keywords + english_keywords
    keyword_counts = Counter(all_keywords)
    
    # Get the most common keywords as tags
    tags = [word for word, count in keyword_counts.most_common(5)]
    
    # Add some common theme tags based on the content
    themes = {
        'success': ['成功', '胜利', '成就', 'success', 'achieve', 'win'],
        'wisdom': ['智慧', '聪明', '明智', 'wisdom', 'smart', 'wise'],
        'perseverance': ['坚持', '毅力', '努力', 'perseverance', 'persist', 'effort'],
        'caution': ['谨慎', '小心', '注意', 'caution', 'careful', 'attention'],
        'friendship': ['友谊', '朋友', '友情', 'friendship', 'friend', 'relationship'],
        'time': ['时间', '时机', '时刻', 'time', 'moment', 'timing'],
        'change': ['变化', '改变', '转变', 'change', 'transform', 'shift'],
        'learning': ['学习', '教育', '知识', 'learn', 'education', 'knowledge']
    }
    
    # Check for theme matches
    for theme, keywords in themes.items():
        if any(keyword in chinese_meaning.lower() or keyword in english_meaning.lower() for keyword in keywords):
            tags.append(theme)
    
    return ';'.join(tags)

def process_idioms():
    """Process idioms and add tags."""
    input_file = 'chinese_idioms_with_translations.csv'
    output_file = 'chinese_idioms_with_tags.csv'
    
    idioms = []
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Generate tags for each idiom
            tags = generate_tags(row['meaning'], row['translation'])
            row['tags'] = tags
            idioms.append(row)
    
    # Write the results to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chinese', 'pinyin', 'meaning', 'translation', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idiom in idioms:
            writer.writerow(idiom)
    
    print(f"Tags generated and saved to {output_file}")

if __name__ == "__main__":
    process_idioms() 