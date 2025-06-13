from docx import Document
import re
import time
import random
import json
import os
import zipfile
import shutil
from lxml import etree
from docx.oxml.shared import OxmlElement
from docx.oxml import ns
from docx.oxml.ns import qn
import pickle

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
nsmap = {"w": W_NS}

def unzip_docx(input_docx, extract_to):
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to)

    with zipfile.ZipFile(input_docx, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def zip_to_docx(folder_path, output_docx):
    with zipfile.ZipFile(output_docx, 'w', zipfile.ZIP_DEFLATED) as docx_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, folder_path)
                docx_file.write(filepath, arcname)

def comment_sentences_by_split_run(input_docx, output_docx, sentences):
    print(f"Processing document: {input_docx}")
    print(f"Number of sentences to process: {len(sentences)}")
    print("First few sentences:")
    for i, sentence in enumerate(sentences[:5]):
        print(f"{i+1}. {sentence}")
    
    temp_dir = "docx_temp"
    unzip_docx(input_docx, temp_dir)

    doc_path = os.path.join(temp_dir, "word", "document.xml")
    doc_tree = etree.parse(doc_path)
    doc_root = doc_tree.getroot()

    comments_path = os.path.join(temp_dir, "word", "comments.xml")
    if os.path.exists(comments_path):
        comments_tree = etree.parse(comments_path)
        comments_root = comments_tree.getroot()
    else:
        comments_root = etree.Element(f"{{{W_NS}}}comments", nsmap=nsmap)
        comments_tree = etree.ElementTree(comments_root)

    paragraphs = doc_root.findall(".//w:body/w:p", namespaces=nsmap)
    print(f"\nFound {len(paragraphs)} paragraphs in document")
    comment_id = 0
    comments_added = 0

    for para_idx, para in enumerate(paragraphs):
        runs = para.findall(".//w:r", namespaces=nsmap)
        if not runs:
            continue

        # Collect all text and their positions
        text_parts = []
        curr_pos = 0
        for run in runs:
            t_elem = run.find(".//w:t", namespaces=nsmap)
            if t_elem is not None and t_elem.text:
                text = t_elem.text
                text_parts.append({
                    'run': run,
                    'text': text,
                    'start': curr_pos,
                    'end': curr_pos + len(text)
                })
                curr_pos += len(text)

        full_text = ''.join(part['text'] for part in text_parts)
        
        if not full_text.strip():
            continue

        # Find and comment each sentence
        for sentence in sentences:
            start_idx = full_text.find(sentence)
            if start_idx == -1:
                continue

            end_idx = start_idx + len(sentence)
            
            # Find runs that contain parts of the sentence
            matching_runs = []
            for part in text_parts:
                if (part['start'] <= end_idx and part['end'] >= start_idx):
                    matching_runs.append(part['run'])

            if not matching_runs:
                continue

            print(f"\nAdding comment for sentence in paragraph {para_idx + 1}:")
            print(f"Text: {sentence}")
            print(f"Found in {len(matching_runs)} runs")

            # Create comment elements
            comment_start = etree.Element(f"{{{W_NS}}}commentRangeStart", {f"{{{W_NS}}}id": str(comment_id)})
            comment_end = etree.Element(f"{{{W_NS}}}commentRangeEnd", {f"{{{W_NS}}}id": str(comment_id)})
            comment_ref = etree.Element(f"{{{W_NS}}}r")
            etree.SubElement(comment_ref, f"{{{W_NS}}}commentReference", {f"{{{W_NS}}}id": str(comment_id)})

            # Insert comment elements
            first_run = matching_runs[0]
            last_run = matching_runs[-1]
            
            # Insert comment start before first run
            first_run.addprevious(comment_start)
            
            # Insert comment end after last run
            last_run.addnext(comment_end)
            last_run.addnext(comment_ref)

            # Create comment content
            comment = etree.SubElement(comments_root, f"{{{W_NS}}}comment", {
                f"{{{W_NS}}}id": str(comment_id),
                f"{{{W_NS}}}author": "GPT",
                f"{{{W_NS}}}date": "2024-03-19T00:00:00Z"
            })
            p = etree.SubElement(comment, f"{{{W_NS}}}p")
            r = etree.SubElement(p, f"{{{W_NS}}}r")
            t = etree.SubElement(r, f"{{{W_NS}}}t")
            t.text = f"Comment on: {sentence}"

            comment_id += 1
            comments_added += 1

    print(f"\nTotal comments added: {comments_added}")

    # Save updated XMLs
    doc_tree.write(doc_path, xml_declaration=True, encoding="utf-8", standalone="yes")
    comments_tree.write(comments_path, xml_declaration=True, encoding="utf-8", standalone="yes")

    # Add relationship to comments.xml
    rels_path = os.path.join(temp_dir, "word", "_rels", "document.xml.rels")
    rels_tree = etree.parse(rels_path)
    rels_root = rels_tree.getroot()
    if not any(rel.attrib.get("Target") == "comments.xml" for rel in rels_root.findall("Relationship")):
        etree.SubElement(rels_root, "Relationship", {
            "Id": "rId100",
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments",
            "Target": "comments.xml"
        })
        rels_tree.write(rels_path, xml_declaration=True, encoding="utf-8", standalone="yes")

    # Add [Content_Types] override
    ct_path = os.path.join(temp_dir, "[Content_Types].xml")
    ct_tree = etree.parse(ct_path)
    ct_root = ct_tree.getroot()
    if not any(el.attrib.get("PartName") == "/word/comments.xml" for el in ct_root.findall("Override")):
        etree.SubElement(ct_root, "Override", {
            "PartName": "/word/comments.xml",
            "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
        })
        ct_tree.write(ct_path, xml_declaration=True, encoding="utf-8", standalone="yes")

    zip_to_docx(temp_dir, output_docx)
    shutil.rmtree(temp_dir)
    print(f"✅ Comments applied and saved: {output_docx}")

if __name__ == "__main__":
    # Test the implementation
    input_path = "input/input.docx"
    output_path = "output.docx"
    
    # Load sentences from pickle file
    with open('sentences.pkl', 'rb') as f:
        sentences = pickle.load(f)
    
    # Apply comments
    comment_sentences_by_split_run(input_path, output_path, sentences) 