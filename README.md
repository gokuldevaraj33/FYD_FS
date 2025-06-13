# Document Comment Generator

A Python tool that adds precise sentence-level comments to Word documents using the Google Gemini API.

## Features

- Processes Word documents (.docx) to add comments at the sentence level
- Uses Google's Gemini AI for intelligent comment generation
- Maintains document formatting and structure
- Handles complex document layouts and formatting

## Requirements

- Python 3.7+
- Required Python packages:
  - python-docx
  - lxml
  - google-generativeai
  - zipfile
  - shutil

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Google Gemini API:
   - Get an API key from Google AI Studio
   - Add your API key to the environment variables or directly in the code

## Usage

1. Place your input document in the `input` folder
2. Run the script:
```bash
python sentence_commenter.py
```

3. The processed document will be saved as `output.docx`

## Project Structure

- `sentence_commenter.py`: Main script for adding comments
- `input/`: Directory for input documents
- `output.docx`: Generated output document
- `sentences.pkl`: Pickle file containing sentences to comment on

## License

MIT License 