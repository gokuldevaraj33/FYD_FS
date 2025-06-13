#!/usr/bin/env python
# coding: utf-8

# In[1]:


import google.generativeai as genai
import os
import docx
import re
import ast


# In[2]:


def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])

file_path = os.path.join("rules", "Academic Research Writing Dos and Don.docx")

example_rules = read_docx(file_path)


# In[3]:


genai.configure(api_key="AIzaSyAKVcYFqUH-SIWpsiz127xE3cZmmgNgG7Y")
model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config={"temperature": 0.0})


# In[4]:


system_prompt = "You are a regex generator. Given writing rules or examples, output Python regex patterns along with their short descriptions to detect them."

user_prompt = f"""
Here are the writing rules or examples:

{example_rules}

Generate Python regex patterns and a short description for each, output as a Python list of dictionaries in the following format:
[
    {{"pattern": r'pattern_here', "description": "short description here"}},
    ...
]
"""
response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
generated_pattern_list = response.text


# In[5]:


validator_system_prompt = """
You are a regex validator and optimizer. Given a list of regex patterns and writing rules:
- Improve the regex patterns if needed.
- Ensure all patterns are case-insensitive by adding (?i) at the start of the pattern.
- Only return a valid Python list of dictionaries.
- Do not include explanations, code comments, or markdown formatting.
- Do not assign the list to any variable.

Return strictly this format:

[
    {"pattern": r'regex_here', "description": "short explanation"},
    ...
]
"""
validator_user_prompt = f"""
Writing Rules:

{example_rules}

Generated Regex Patterns:

{generated_pattern_list}

Please review and improve the patterns. Return the updated list in this format:

[
    {{"pattern": r'pattern_here', "description": "short description here"}},
    ...
]
"""

response = model.generate_content(f"{validator_system_prompt}\n\n{validator_user_prompt}")
validated_pattern_list = response.text


# In[12]:


import re
import ast

# Initialize early so it's always defined
global parsed_pattern_list
parsed_pattern_list= []

list_match = re.search(r'(\[.*\])', validated_pattern_list, re.DOTALL)

if list_match:
    clean_list_str = list_match.group(1)
    try:
        parsed_pattern_list = ast.literal_eval(clean_list_str)
    except Exception as e:
        parsed_pattern_list = []


# In[14]:


import json

with open("parsed_pattern_list.json", "w") as f:
    json.dump(parsed_pattern_list, f, indent=2)


# In[ ]:




