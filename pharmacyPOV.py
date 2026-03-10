import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import os

DATA_FOLDER = "Data"
COL_NAME = 3

# Import your existing search functions
def get_file_path(medicine_name):
    if not medicine_name:
        return None
    first_letter = medicine_name[0].upper()
    return f"{DATA_FOLDER}/{first_letter}/{first_letter}_medicines.csv"

def binary_search(rows, target_name, col_name=COL_NAME):
    low = 0
    high = len(rows) - 1
    target = target_name.strip().lower()
    
    while low <= high:
        mid = (low + high) // 2
        try:
            mid_val = rows[mid][col_name].strip().lower()
        except IndexError:
            mid_val = ""
        if mid_val == target:
            return rows[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Doctor POV columns
DOC_COL_COMPOSITION = 15
DOC_COL_USES = 20
DOC_COL_SIDE_EFFECTS = 22

# Customer POV columns
CUST_COL_USES = 20
CUST_COL_HOW_TO_USE = 23
CUST_COL_SIDE_EFFECTS = 22
CUST_COL_FAQS = 27

# Pharmacy POV columns
PHARM_COL_SHORT_COMP = 15
PHARM_COL_COMPOSITION = 40
PHARM_COL_MRP = 10
PHARM_COL_PACK = 5

def search_doctor_pov(medicine_name):
    file_path = get_file_path(medicine_name)
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found"
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            rows = list(reader)
            result_row = binary_search(rows, medicine_name)
            
            if result_row:
                comp = result_row[DOC_COL_COMPOSITION] if len(result_row) > DOC_COL_COMPOSITION else "N/A"
                uses = result_row[DOC_COL_USES] if len(result_row) > DOC_COL_USES else "N/A"
                side_eff = result_row[DOC_COL_SIDE_EFFECTS] if len(result_row) > DOC_COL_SIDE_EFFECTS else "N/A"
                
                return f"""DOCTOR VIEW
{"="*60}
Medicine: {result_row[COL_NAME]}

COMPOSITION:
{comp}

USES:
{uses}

SIDE EFFECTS:
{side_eff}
{"="*60}"""
            else:
                return f"Medicine '{medicine_name}' not found"
    except Exception as e:
        return f"Error: {str(e)}"

def search_customer_pov(medicine_name):
    file_path = get_file_path(medicine_name)
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found"
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            next(reader)
            rows = list(reader)
            result_row = binary_search(rows, medicine_name)
            
            if result_row:
                uses = result_row[CUST_COL_USES] if len(result_row) > CUST_COL_USES else "N/A"
                how_to = result_row[CUST_COL_HOW_TO_USE] if len(result_row) > CUST_COL_HOW_TO_USE else "N/A"
                side_eff = result_row[CUST_COL_SIDE_EFFECTS] if len(result_row) > CUST_COL_SIDE_EFFECTS else "N/A"
                faqs = result_row[CUST_COL_FAQS] if len(result_row) > CUST_COL_FAQS else "N/A"
                
                return f"""CUSTOMER VIEW
{"="*60}
Medicine: {result_row[COL_NAME]}

USES:
{uses}

HOW TO USE:
{how_to}

SIDE EFFECTS:
{side_eff}

FAQs:
{faqs}
{"="*60}"""
            else:
                return f"Medicine '{medicine_name}' not found"
    except Exception as e:
        return f"Error: {str(e)}"

def search_pharmacy_pov(medicine_name):
    file_path = get_file_path(medicine_name)
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found"
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            next(reader)
            rows = list(reader)
            result_row = binary_search(rows, medicine_name)
            
            if result_row:
                short_comp = result_row[PHARM_COL_SHORT_COMP] if len(result_row) > PHARM_COL_SHORT_COMP else "N/A"
                composition = result_row[PHARM_COL_COMPOSITION] if len(result_row) > PHARM_COL_COMPOSITION else "N/A"
                mrp = result_row[PHARM_COL_MRP] if len(result_row) > PHARM_COL_MRP else "N/A"
                pack = result_row[PHARM_COL_PACK] if len(result_row) > PHARM_COL_PACK else "N/A"
                
                return f"""PHARMACY VIEW
{"="*60}
Medicine: {result_row[COL_NAME]}

SHORT COMPOSITION:
{short_comp}

FULL COMPOSITION:
{composition}

MRP:
{mrp}

PACK INFORMATION:
{pack}
{"="*60}"""
            else:
                return f"Medicine '{medicine_name}' not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_medicines_starting_with(letter):
    """Get medicines only from specific letter folder"""
    medicines = []
    folder_path = os.path.join(DATA_FOLDER, letter.upper())
    
    if not os.path.exists(folder_path):
        return medicines
    
    csv_file = os.path.join(folder_path, f"{letter.upper()}_medicines.csv")
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) > COL_NAME:
                        medicines.append(row[COL_NAME])
        except Exception as e:
            print(f"Error: {e}")
    
    return medicines

class MedicineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Information System")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        # Title
        title = tk.Label(root, text="🏥 Medicine Information System", 
                        font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=20)
        
        # View Type Selection
        view_frame = tk.Frame(root, bg="#f0f0f0")
        view_frame.pack(pady=15)
        
        tk.Label(view_frame, text="Select View:", font=("Arial", 12, "bold"), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.view_var = tk.StringVar(value="Customer")
        view_dropdown = ttk.Combobox(view_frame, textvariable=self.view_var, 
                                     values=["Customer", "Pharmacy", "Doctor"],
                                     state="readonly", width=15, font=("Arial", 11))
        view_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Medicine Search Box
        search_frame = tk.Frame(root, bg="#f0f0f0")
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Medicine Name:", font=("Arial", 12, "bold"), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                     width=45, font=("Arial", 11))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Suggestions Listbox
        suggest_label = tk.Label(root, text="Suggestions:", font=("Arial", 10), 
                                bg="#f0f0f0", fg="#666")
        suggest_label.pack(pady=(10,5))
        
        self.suggestions_frame = tk.Frame(root, bg="#f0f0f0")
        self.suggestions_frame.pack(pady=5)
        
        self.suggestions_listbox = tk.Listbox(self.suggestions_frame, width=65, height=6, 
                                             font=("Arial", 10))
        self.suggestions_listbox.pack(side=tk.LEFT)
        self.suggestions_listbox.bind('<<ListboxSelect>>', self.on_select_suggestion)
        
        scrollbar = tk.Scrollbar(self.suggestions_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.suggestions_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.suggestions_listbox.yview)
        
        # Search Button
        search_btn = tk.Button(root, text="🔍 Search", font=("Arial", 14, "bold"),
                              bg="#3498db", fg="white", padx=40, pady=12,
                              command=self.search, cursor="hand2")
        search_btn.pack(pady=20)
        
        # Result Text Area
        result_label = tk.Label(root, text="Results:", font=("Arial", 12, "bold"), 
                               bg="#f0f0f0")
        result_label.pack(pady=5)
        
        self.result_text = scrolledtext.ScrolledText(root, height=18, width=95, 
                                                     wrap=tk.WORD, font=("Courier", 10))
        self.result_text.pack(pady=10, padx=20)
        
        self.current_suggestions = []
    
    def on_search_change(self, *args):
        search_term = self.search_var.get().strip()
        
        if len(search_term) < 1:
            self.suggestions_listbox.delete(0, tk.END)
            self.current_suggestions = []
            return
        
        first_letter = search_term[0].upper()
        medicines = get_medicines_starting_with(first_letter)
        filtered = [m for m in medicines if search_term.lower() in m.lower()][:50]
        
        self.suggestions_listbox.delete(0, tk.END)
        self.current_suggestions = filtered
        
        for med in filtered:
            self.suggestions_listbox.insert(tk.END, med)
    
    def on_select_suggestion(self, event):
        selection = self.suggestions_listbox.curselection()
        if selection:
            index = selection[0]
            selected = self.suggestions_listbox.get(index)
            self.search_var.set(selected)
    
    def search(self):
        medicine = self.search_var.get().strip()
        view_type = self.view_var.get()
        
        if not medicine:
            messagebox.showwarning("Warning", "Please enter a medicine name")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Searching...\n")
        self.root.update()
        
        # Call appropriate search function based on view type
        if view_type == "Doctor":
            result = search_doctor_pov(medicine)
        elif view_type == "Customer":
            result = search_customer_pov(medicine)
        elif view_type == "Pharmacy":
            result = search_pharmacy_pov(medicine)
        else:
            result = "Invalid view type"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineApp(root)
    root.mainloop()