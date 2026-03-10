import csv
import os

DATA_FOLDER = "Data"  
COL_NAME = 3           # title column
COL_USES = 20          # uses
COL_HOW_TO_USE = 23    # howToUse
COL_SIDE_EFFECTS = 22  # sideEffects
COL_FAQS = 27          # faqs

def get_file_path(medicine_name):
    if not medicine_name:
        return None
    
    first_letter = medicine_name[0].upper()
    return f"{DATA_FOLDER}/{first_letter}/{first_letter}_medicines.csv"

def binary_search(rows, target_name):
    low = 0
    high = len(rows) - 1
    target = target_name.strip().lower()
    
    while low <= high:
        mid = (low + high) // 2
        
        try:
            mid_val = rows[mid][COL_NAME].strip().lower()
        except IndexError:
            mid_val = ""
            
        if mid_val == target:
            return rows[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return None

def search_medicine_customer():
    print("--- Customer Medicine Info ---")
    print(f"Looking for CSV files in folder: '{DATA_FOLDER}/'")
    
    while True:
        med_input = input("\nEnter Medicine Name (or 'q' to quit): ").strip()
        
        if med_input.lower() == 'q':
            print("Exiting...")
            break
            
        if not med_input:
            continue
            
        file_path = get_file_path(med_input)
        
        if not os.path.exists(file_path):
            print(f"Error: File not found ({file_path}).")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                
                try:
                    header = next(reader) 
                except StopIteration:
                    print("Error: The CSV file appears to be empty.")
                    continue
                    
                rows = list(reader)
                
                result_row = binary_search(rows, med_input)
                
                if result_row:
                    print("\n--- Found Match ---")
                    print(f"Medicine:       {result_row[COL_NAME]}")
                    
                    uses = result_row[COL_USES] if len(result_row) > COL_USES else "N/A"
                    how_to = result_row[COL_HOW_TO_USE] if len(result_row) > COL_HOW_TO_USE else "N/A"
                    side_eff = result_row[COL_SIDE_EFFECTS] if len(result_row) > COL_SIDE_EFFECTS else "N/A"
                    faqs = result_row[COL_FAQS] if len(result_row) > COL_FAQS else "N/A"
                    
                    print(f"Uses:           {uses[:]}...")  
                    print(f"How to Use:     {how_to[:]}...")
                    print(f"Side Effects:   {side_eff[:]}...")
                    print(f"FAQs:           {faqs[:]}...")
                else:
                    print(f"Result: '{med_input}' not found in {file_path}.")
                    
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        print(f"Created '{DATA_FOLDER}' directory.")
    
    search_medicine_customer()