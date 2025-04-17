import pandas as pd
import os
from openpyxl import load_workbook

# Load the Excel file
file_path = r'c:\Users\aleaf\OneDrive\Desktop\Woodbridge - 4_1_2025.xlsx'  
df = pd.read_excel(file_path)

# Define a list of keywords that indicate a company
company_keywords = ["LLC", "Inc", "Corp", "Ltd", "Co.", "Group", "Enterprises"]  # Add your own!

# Function to check if a name is a company
def is_company(name):
    return any(keyword.lower() in str(name).lower() for keyword in company_keywords)

# Update the existing 'Type' column: label companies as "Commercial" and personal names as "Personal"
df.loc[df['Name'].apply(is_company), 'Type'] = 'Commercial'  # Label company names as "Commercial"
df.loc[~df['Name'].apply(is_company), 'Type'] = 'Personal'   # Label personal names as "Personal"

# Sort ONLY by 'Type' and 'Name', keeping other columns unchanged
df = df.sort_values(by=['Type', 'Name'], ascending=[True, True], ignore_index=False)

# Save the sorted data to Excel without modifying column formatting
df.to_excel(file_path, index=False)  

# Load the workbook using openpyxl to adjust column widths
wb = load_workbook(file_path)
ws = wb.active  # Get the active sheet

# Adjust column width based on the longest content in each column
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter  # Get the column letter (e.g., A, B, C)
    for cell in col:
        try:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        except:
            pass
    adjusted_width = max_length + 2  # Add some extra space for padding
    ws.column_dimensions[col_letter].width = adjusted_width  

# Save the updated workbook with adjusted column width
wb.save(file_path)

print("Excel file has been updated! Columns are now auto-sized for better readability.")

# Open the Excel file after formatting is applied
os.startfile(file_path)