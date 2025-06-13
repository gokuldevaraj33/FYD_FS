from docx import Document
import re
import time
import random

# === Patterns ===
REFERENCES_PATTERN = re.compile(
    r"^(list\s+of\s+)?(references|bibliography|works\s+cited)\s*$", re.IGNORECASE
)

EXCLUDE_PREFIXES = re.compile(r"^(name|student name|date|course|section|professor|instructor)[\s:]", re.IGNORECASE)

QUESTION_KEYWORDS = [
    "what", "why", "how", "when", "where", "which", "who", "whom", "whose", "is", "are", "can", "could", "should",
    "would", "will", "do", "does", "did", "explain", "define", "describe", "elaborate", "compare", "contrast",
    "discuss", "illustrate", "analyze", "interpret", "evaluate", "examine", "assess", "outline", "summarize",
    "state", "list", "enumerate", "identify", "classify", "relate", "demonstrate", "justify", "argue", "prove",
    "predict", "formulate", "construct", "design", "develop", "support", "review", "trace", "distinguish",
    "differentiate", "explore", "investigate", "highlight", "indicate", "determine", "specify", "reason",
    "elucidate", "delve", "clarify", "reveal", "uncover", "break down", "find", "guess", "present", "recommend",
    "suggest", "mention", "focus", "restate", "note", "point out", "consider", "reflect", "recall", "name",
    "show", "solve", "address", "assume", "depict", "respond", "resolve", "decide", "conclude", "extend",
    "simplify", "transform", "probe", "look into", "throw light on", "if", "how far", "to what extent",
    "in what ways", "examine how", "examine why", "analyze how", "assess whether", "critically evaluate",
    "debate whether", "explain whether", "why do you think", "what do you think", "is it possible", 
    "should we", "how would you", "can we say", "would you agree", "what are the reasons", 
    "how does", "why does", "what happens", "if you were", "can you explain", "why is it important",
    "do you believe", "why might", "what could", "what would happen", "how important", 
    "if so", "if not", "is that true", "how can", "what impact", "what role", "how much", 
    "why should", "should it be", "in your opinion", "what evidence", "how would", 
    "what kind", "which factors", "how effective", "how likely", "is there any", "does it make sense"
]

QUESTION_REGEX_PATTERN = re.compile(
    r"^(\d+[\).]?\s*)?((Q[\.:)]?)?\s*)?(" + "|".join(re.escape(k) for k in QUESTION_KEYWORDS) + r")\b.+", re.IGNORECASE
)

def is_references_section(text):
    text = text.strip().lower()
    return bool(re.match(r"^(list of references|references|bibliography|works cited)[\s:]*$", text))

# === Load all usable paragraphs ===
def load_paragraphs_until_references(file_path):
    doc = Document(file_path)
    paragraphs = []
    for para in doc.paragraphs:
        if is_references_section(para.text):
            break
        if para.text.strip():
            paragraphs.append(para)
    return paragraphs

def process_docx_to_qa_list():
    paragraphs = load_paragraphs_until_references("input.docx")
    return [{"question": q, "answer": a} for q, a in zip(*extract_qa_pairs(paragraphs))]

def extract_qa_pairs(paragraphs):
    questions = []
    answers = []
    current_question = None
    current_answer = []
    previous_was_question = False

    for para in paragraphs:
        if is_question_line(para, previous_was_question):
            if current_question:
                questions.append(current_question.text.strip())
                answers.append("\n".join(p.text.strip() for p in current_answer))
                current_answer = []
            current_question = para
            previous_was_question = True
        elif current_question:
            if is_continuation_of_answer(para, current_question.text):
                current_answer.append(para)
            else:
                current_answer.append(para)
            previous_was_question = False

    if current_question:
        questions.append(current_question.text.strip())
        answers.append("\n".join(p.text.strip() for p in current_answer))

    return questions, answers

def is_continuation_of_answer(para, last_question_text):
    text = para.text.strip()
    lower_text = text.lower()

    if re.search(r"\([\w\s&\-,]+,\s*\d{4}\)", text):
        return True
    if re.match(r"^[A-Z][\w\s\-]{2,40}:\s*$", text):
        return True
    if re.match(r"^\(?[A-Ca-c]\)?\s*[\w\s\-]{2,40}:\s*$", text):
        return True
    if len(text.split()) <= 12 and text.endswith('.') and text[0].isupper():
        return True
    if re.match(r"^\(?[A-Ca-c]\)?\s", text) and not any(k in lower_text for k in QUESTION_KEYWORDS):
        return True
    if re.match(r"^\d+[\).]", text) and any(k in last_question_text.lower() for k in ["list", "identify", "write about", "examples", "steps"]):
        return True

    return False

QUESTION_LONG_PATTERN = re.compile(
    r"^\d{1,2}[\).]?\s*(if|would|should|could|what|why|how|when|where|who|do|does|did|is|are|can|will|explain|describe|discuss|evaluate|list|identify|name|write|state|mention|give|define|elaborate|specify)\b.*",
    re.IGNORECASE
)

def passes_question_validation(text):
    if QUESTION_LONG_PATTERN.match(text):
        return True
    if text.endswith('?'):
        return True
    if QUESTION_REGEX_PATTERN.match(text):
        return True
    if re.match(r"^(\d+[\).]|[-*])\s", text):
        return True
    return False


def is_question_line(para, previous_question_detected):
    text = para.text.strip()
    lower_text = text.lower()
    words = text.split()

    print(f"\n[CHECKING]: {text}")

    if not text or len(words) < 3:
        print("→ ❌ Excluded: too short or empty")
        return False

    if EXCLUDE_PREFIXES.match(text):
        print("→ ❌ Excluded: matches EXCLUDE_PREFIXES")
        return False

    if re.match(r"^[A-Z]{2,}\s*[-–]\s*\d+", text):
        print("→ ❌ Excluded: course code format")
        return False

    if lower_text.startswith(("writing assignment", "list of references")):
        print("→ ❌ Excluded: writing assignment or references section")
        return False

    if re.match(r"^q\d+[:\.)]?\s*(references|list of references)$", lower_text):
        print("→ ❌ Excluded: fake Q-label for references")
        return False

    if all(w.isalpha() for w in words) and text.isupper():
        print("→ ❌ Excluded: all uppercase heading")
        return False

    if re.match(r"^\(?[A-Ca-c]\)?\s*[\w\s\-]{1,40}:\s*$", text):
        print("→ ❌ Excluded: side heading like (A) Topic:")
        return False

    if re.match(r"^[A-Z][\w\s\-]{2,40}:\s*$", text):
        print("→ ❌ Excluded: short heading ending in colon")
        return False

    if lower_text.strip() in {"assignment", "worksheet", "homework", "references", "list of references", "bibliography"}:
        print("→ ❌ Excluded: full paragraph is academic admin word")
        return False

    if re.match(r"^\d{1,2}\s*[\).]?\s*(if|would|should|could|what|why|how|when|where|who|do|does|did|is|are|can|will)\b", lower_text):
        print("→ ✅ Included: starts with number and question word")
        return True

    if text.endswith('?'):
        print("→ ✅ Included: ends with question mark")
        return True

    if QUESTION_REGEX_PATTERN.match(text):
        print("→ ✅ Included: matches QUESTION_REGEX_PATTERN")
        return True

    if re.match(r"^(\d+[\).]|[-*])\s", text):
        print("→ ✅ Included: starts with list-style numbering")
        return True

    if re.match(r"^\d{1,2}\s*[\).]?\s*(%s)\b" % "|".join(QUESTION_KEYWORDS), lower_text):
        print("→ ✅ Included: starts with numbered question keyword")
        return True

    if (
        any(run.bold for run in para.runs if run.text.strip()) and
        not text.endswith(':') and
        not re.match(r"^[A-Z][\w\s\-]{2,40}:\s*", text) and
        len(words) >= 6 and
        any(kw in lower_text for kw in QUESTION_KEYWORDS) and
        not re.search(r"\([\w\s&\-,]+,\s*\d{4}\)", text)  # contains citation? then it's answer
    ):
        print("→ ✅ Included: bold with keyword, not subheading, no citation")
        return True

    print("→ ❌ Not a question")
    return False

qa_list = process_docx_to_qa_list()

for idx, qa in enumerate(qa_list, 1):
    print(f"Q{idx}: {qa['question']}")
    print(f"A{idx}: {qa['answer']}")
    print("-" * 60)
    
def clean_fragmented_words(sentences):
    """Fix broken words across split lines, e.g., 'Potent', 'ial' → 'Potential'"""
    fixed = []
    i = 0
    while i < len(sentences):
        current = sentences[i]
        # If the sentence is too short and next exists, try merging
        if len(current) < 15 and i + 1 < len(sentences):
            merged = current + ' ' + sentences[i + 1]
            fixed.append(merged.strip())
            i += 2
        else:
            fixed.append(current.strip())
            i += 1
    return fixed

import re

import re

def split_answers(qa_list):
    all_answer_sentence_groups = []

    abbreviations = ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sr.', 'Jr.', 'St.', 'vs.', 'e.g.', 'i.e.', 'etc.']
    placeholder = '§§§'

    # Pattern to detect and strip subheadings like (A) Topic: or A) Topic:
    subheading_strip_pattern = re.compile(r"^\(?[A-Ca-c]\)?\s*[\w\s\-]{1,40}:\s*", re.IGNORECASE)

    for qa in qa_list:
        answer = qa['answer']

        # Protect abbreviations
        for abbr in abbreviations:
            answer = answer.replace(abbr, abbr.replace('.', placeholder))

        # Split into sentences (basic rule: punctuation followed by capital)
        sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])', answer.strip())

        cleaned_sentences = []
        for s in sentences:
            s = s.replace(placeholder, '.').strip()
            # Strip subheading at the beginning, but keep the actual sentence
            s = subheading_strip_pattern.sub('', s)
            if s:
                cleaned_sentences.append(s)

        all_answer_sentence_groups.append(cleaned_sentences)

    return all_answer_sentence_groups


answer_sentences = split_answers(qa_list)
for group in answer_sentences:
    print(group)
