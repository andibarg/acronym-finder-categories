#!/usr/bin/env python

"""Script to find acronyms in a word doc or docx file.""" 

import os
from datetime import datetime
import pandas as pd
import re
import docx
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Browse for word file
Tk().withdraw()
filename = askopenfilename(filetypes=[("Microsoft Word files", ".doc .docx")],
                           initialdir=os.getcwd())

# Path to all lists
folder = os.path.join(os.getcwd(),'lists')

# File all files and skip temp Excel files
allfiles = os.listdir(folder)
allfiles = [file for file in allfiles if not file.startswith('~$')]

# Function to find duplicates in lowercase strings
def find_duplicates_lowercase(df, columns, keep='first'):
    df_lower = df.copy()
    for column in columns:
        df_lower[column] = df[column].str.lower()
    dupes = df_lower.duplicated(subset=columns,keep=keep)
    return dupes

# Go through lists
print('\nLoading lists ...\n')
for ii, file in enumerate(allfiles):   
    # Get file name and extension
    print(file)
    name, ext = os.path.splitext(file)

    # Read file if possible
    if ext == '.csv':
        df0 = pd.read_csv(os.path.join(folder,file))
    elif ext == '.xlsx':
        df0 = pd.read_excel(os.path.join(folder,file))
    else:
        continue

    # Drop duplicates and sort within category
    dupes = find_duplicates_lowercase(df0,['Acronym','Definition'])
    df0 = df0[~dupes]
    df0 = df0.sort_values(by=['Acronym','Definition'])

    # Save file
    if ext == '.csv':
        df0.to_csv(os.path.join(folder,file),index=False,sep=',')
    elif ext == '.xlsx':
        df0.to_excel(os.path.join(folder,file),index=False)

    # Add category column
    df0['Category'] = name

    # Append to combined dataframe
    if ii == 0:
        df = df0
    else:
        df = pd.concat([df, df0])

# Join categories for duplicates
df = df.groupby([df['Acronym'].str.lower(),df['Definition'].str.lower()],
                as_index=False).agg({'Acronym':'first','Definition':'first',
                                     'Category':", ".join})

# Open docx file
doc = docx.Document(filename)

fullText = []
for para in doc.paragraphs:
    fullText.append(para.text)
fullText = ''.join(fullText)

# Loop through all acronyms
acronyms_doc = []
print('\nFind all acronyms in document ...')
for ii, acronym in enumerate(df.Acronym):
    # Search acronym
    prog = re.compile('\W%s\W' %acronym, flags=re.IGNORECASE)
    result = prog.findall(fullText)

    # Add to list
    if len(result) > 0:
        acronyms_doc.append([acronym, df.Definition[ii]])

# Save as Excel
print('\nSaving Excel list ...')
df_doc = pd.DataFrame(acronyms_doc)
df_doc.columns = ['Acronyms','Definitions']
df_doc.to_excel(os.path.splitext(filename)[0] + '.xlsx',
                index=False)

print('\nDone!')
