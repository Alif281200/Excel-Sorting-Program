import pandas as pd
import os
import datetime
from openpyxl import load_workbook

# Folder where Excel files are stored
input_folder = r'c:\Users\aleaf\Downloads\Tax Copies'  # Change this to your actual folder path

# Generate unique filenames with timestamps to avoid permission issues
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file_path = os.path.join(input_folder, f"Merged_Sorted_Data_{timestamp}.xlsx")
personal_file_path = os.path.join(input_folder, f"Personal_Only_{timestamp}.xlsx")

# Define keywords that indicate a company
company_keywords = ["LLC", "Inc", "Corp", "Ltd", "Co.", "Group", "Enterprises", "Church", "TRST%" 
                    "Iglesia", " L L C", "CORP", "C O", "COVE","TRUSTEE", "REALTY", "CSX"
                    "LOCAL", "L&C", "D&C", "TRUST", "FELLOWSHIP", "EXECUTOR", "AMTRAK", "LP", "CO"
                    "ET AL", "ET ALS" "GURDIT", "LODGING"]

# Function to check if a name is a company
def is_company(name):
    return any(keyword.lower() in str(name).lower() for keyword in company_keywords)

# Function to extract city name from file name
def extract_city(file_name):
    city = os.path.basename(file_name).split()[0]  # Extracts first word as city
    return city

# List to store DataFrames
merged_data = []

# Process all Excel files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xlsx") and not file_name.startswith("~$"):  # Ignore temp files
        input_file_path = os.path.join(input_folder, file_name)

        # Read the Excel file
        df = pd.read_excel(input_file_path)

        # Extract city name from file name
        city_name = extract_city(file_name)

        # Update the existing 'Type' column
        df.loc[df['Name'].apply(is_company), 'Type'] = 'Commercial'
        df.loc[~df['Name'].apply(is_company), 'Type'] = 'Personal'

        # Add a new "City" column
        df["City"] = city_name

        # Keep only the required columns
        selected_columns = ["City", "Type", "Name", "Address", "Money Owed"]
        df_filtered = df[selected_columns]

        # Remove rows where "Name" is empty (to clean up empty Personal entries)
        df_filtered = df_filtered.dropna(subset=["Name"])

        # Add DataFrame to the list
        merged_data.append(df_filtered)

# Combine all data into one DataFrame
final_df = pd.concat(merged_data, ignore_index=True)

# Sort by 'Type' first (Personal first, then Commercial), then by 'Name'
final_df = final_df.sort_values(by=['Type', 'Name'], ascending=[True, True], ignore_index=True)

# Save merged data to a new Excel file
final_df.to_excel(output_file_path, index=False)

# Save only "Personal" entries into a separate file
personal_df = final_df[final_df["Type"] == "Personal"]
personal_df.to_excel(personal_file_path, index=False)

# Load the new workbook to adjust column width
for file in [output_file_path, personal_file_path]:
    wb = load_workbook(file)
    ws = wb.active  

    # Auto-adjust column width
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2  

    # Save the updated workbook with adjusted column widths
    wb.save(file)

print(f"✅ Merged sorted data saved as '{output_file_path}'")
print(f"✅ Personal-only list saved as '{personal_file_path}'")

# Open both files after processing
os.startfile(output_file_path)
os.startfile(personal_file_path)
