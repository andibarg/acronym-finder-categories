import os
from datetime import datetime
import pandas as pd

# Path to all lists
folder = os.path.join(os.getcwd(),'lists')

# Go through lists
print('\nLoading lists ...\n')
for ii, file in enumerate(os.listdir(folder)):   
    # Get file name and extension
    print(file)
    name, ext = os.path.splitext(file)
    if name == 'General':
        name = ''

    # Read file if possible
    if ext == '.csv':
        df0 = pd.read_csv(os.path.join(folder,file))
    elif ext == '.xlsx':
        df0 = pd.read_excel(os.path.join(folder,file))
    else:
        continue

    # Add category column
    df0['Category'] = name

    # Drop duplicates within category
    df0 = df0.drop_duplicates()

    # Append to dataframe
    if ii == 0:
        df = df0
    else:
        df = pd.concat([df, df0])

# Find duplicates across categories
dupes = df.duplicated(subset=['Acronym','Definition'],keep=False)
df['Category'][dupes] = ''
df = df.drop_duplicates(subset=['Acronym','Definition'])

# Sort alphabetically
df = df.sort_values(by='Acronym')

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
        file.write(row)
    file.write(']\n')

    # Add date variable
    datevar = 'var lastUpdate = "%s";'
    file.write(datevar %datetime.today().strftime('%B %d, %Y'))
print('\nDone!')
