# Chinese Idioms Project

This project processes Chinese idioms, translates them, and generates topic tags based on their meanings.

## Setup

1. Make sure you have Python 3.x installed
2. Run the setup script to create and activate the virtual environment:
   ```bash
   ./setup.sh
   ```
   This will:
   - Create a virtual environment if it doesn't exist
   - Activate the virtual environment
   - Install all required dependencies

3. To activate the virtual environment in future sessions:
   ```bash
   source venv/bin/activate
   ```

## Project Structure

- `chinese_idioms.csv`: Original Chinese idioms data
- `chinese_idioms_with_translations.csv`: Idioms with English translations
- `chinese_idioms_with_tags.csv`: Idioms with translations and generated tags
- `generate_tags.py`: Script to generate topic tags for idioms
- `requirements.txt`: Python package dependencies
- `setup.sh`: Setup script for virtual environment

## Usage

After setting up the environment, you can run the tag generation script:
```bash
python3 generate_tags.py
```

This will process the idioms and generate a new CSV file with topic tags based on both Chinese and English meanings. 