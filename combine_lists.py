#!/usr/bin/env python

"""Script to combine and save acronym lists (csv or xlsx).""" 

import os
from datetime import datetime
import pandas as pd

# Path to all lists
folder = os.path.join(os.getcwd(),'lists')

# Find all files and skip temp Excel files
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

# Write javascript file
acronym_list = os.path.join(os.getcwd(),'acronym_list.js')
print('\nSaving combined list ...')
with open('acronym_list.js', 'w') as file:
    # Fill text
    file.write('var acronymList = [\n')

    # Write rows
    for ii in range(len(df)):
        row = ('  {"acronym":"%s",'
               '"term":"%s",'
               '"category":"%s"},\n')
        row = row %tuple(df.iloc[ii][['Acronym',
                                      'Definition',
                                      'Category']])
        
        # Convert special characters
        row = row.encode("ascii", "xmlcharrefreplace").decode("utf-8")
        
        file.write(row)
    file.write(']\n')

    # Add date variable
    datevar = 'var lastUpdate = "%s";'
    file.write(datevar %datetime.today().strftime('%B %d, %Y'))
print('\nDone!')
