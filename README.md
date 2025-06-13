# Document Comment Generator

A Python tool that adds precise sentence-level comments to Word documents using the Google Gemini API.

## Project Structure

```
FYD_FS/
├── backend/               # Python scripts and data files
│   ├── sentence_commenter.py
│   ├── gemini_api_model.py
│   ├── extract_answers.py
│   ├── parsed_pattern_list.json
│   ├── sentence_analysis_dict.json
│   └── sentences.pkl
├── notebooks/            # Jupyter notebooks
│   ├── main.ipynb
│   ├── cmt_testing.ipynb
│   ├── commenting.ipynb
│   ├── FYD_Gokul.ipynb
│   └── gemini_api_model.ipynb
├── input/               # Input documents
│   ├── input.docx
│   ├── input1.docx
│   ├── input2.docx
│   └── input_no_que.docx
├── output/             # Generated output documents
│   └── output.docx
├── rules/             # Writing rules and patterns
│   └── Academic Research Writing Dos and Don.docx
├── .gitignore
├── README.md
└── requirements.txt
```

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
git clone https://github.com/gokuldevaraj33/FYD_FS.git
cd FYD_FS
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
python backend/sentence_commenter.py
```

3. The processed document will be saved in the `output` folder

## License

MIT License 