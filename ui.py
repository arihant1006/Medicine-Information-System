import streamlit as st
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
PHARM_COL_MRP = 9
PHARM_COL_PACK = 5

def search_doctor_pov(medicine_name):
    file_path = get_file_path(medicine_name)
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found", False
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            next(reader)
            rows = list(reader)
            result_row = binary_search(rows, medicine_name)
            
            if result_row:
                comp = result_row[DOC_COL_COMPOSITION] if len(result_row) > DOC_COL_COMPOSITION else "N/A"
                uses = result_row[DOC_COL_USES] if len(result_row) > DOC_COL_USES else "N/A"
                side_eff = result_row[DOC_COL_SIDE_EFFECTS] if len(result_row) > DOC_COL_SIDE_EFFECTS else "N/A"
                
                return {
                    'name': result_row[COL_NAME],
                    'composition': comp,
                    'uses': uses,
                    'side_effects': side_eff
                }, True
            else:
                return f"Medicine '{medicine_name}' not found", False
    except Exception as e:
        return f"Error: {str(e)}", False

def search_customer_pov(medicine_name):
    file_path = get_file_path(medicine_name)
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found", False
    
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
                
                return {
                    'name': result_row[COL_NAME],
                    'uses': uses,
                    'how_to_use': how_to,
                    'side_effects': side_eff,
                    'faqs': faqs
                }, True
            else:
                return f"Medicine '{medicine_name}' not found", False
    except Exception as e:
        return f"Error: {str(e)}", False

def search_pharmacy_pov(medicine_name):
    file_path = get_file_path(medicine_name)
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found", False
    
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
                
                return {
                    'name': result_row[COL_NAME],
                    'short_composition': short_comp,
                    'full_composition': composition,
                    'mrp': mrp,
                    'pack': pack
                }, True
            else:
                return f"Medicine '{medicine_name}' not found", False
    except Exception as e:
        return f"Error: {str(e)}", False

@st.cache_data
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
            st.error(f"Error: {e}")
    
    return sorted(medicines)

@st.cache_data
def get_all_medicines():
    """Get all medicine names (cached)"""
    all_meds = []
    if not os.path.exists(DATA_FOLDER):
        return all_meds
    
    for folder in os.listdir(DATA_FOLDER):
        folder_path = os.path.join(DATA_FOLDER, folder)
        if os.path.isdir(folder_path):
            meds = get_medicines_starting_with(folder)
            all_meds.extend(meds)
    
    return sorted(all_meds)

# Streamlit UI
st.set_page_config(page_title="Medicine Information System", page_icon="🏥", layout="wide")

st.title("🏥 Medicine Information System")
st.markdown("---")

# Sidebar for view selection
with st.sidebar:
    st.header("Settings")
    view_type = st.selectbox(
        "Select View",
        ["Customer", "Pharmacy", "Doctor"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
    ### Views Explained:
    - **Customer**: Uses, How to Use, Side Effects, FAQs
    - **Pharmacy**: Composition, MRP, Pack Info
    - **Doctor**: Composition, Uses, Side Effects
    """)

# Medicine search
col1, col2 = st.columns([3, 1])

with col1:
    # Get all medicines for autocomplete
    all_medicines = get_all_medicines()
    
    if all_medicines:
        medicine_name = st.selectbox(
            "Search Medicine",
            options=[""] + all_medicines,
            help="Start typing to filter medicines"
        )
    else:
        medicine_name = st.text_input("Enter Medicine Name", "")
        st.warning("⚠️ Medicine database not found. Please check the Data folder.")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

st.markdown("---")

# Search functionality
if search_button or medicine_name:
    if not medicine_name:
        st.warning("⚠️ Please select a medicine name")
    else:
        with st.spinner("Searching..."):
            if view_type == "Doctor":
                result, success = search_doctor_pov(medicine_name)
                
                if success:
                    st.success(f"✅ Found: **{result['name']}**")
                    
                    tab1, tab2, tab3 = st.tabs(["📋 Composition", "💊 Uses", "⚠️ Side Effects"])
                    
                    with tab1:
                        st.subheader("Composition")
                        st.write(result['composition'])
                    
                    with tab2:
                        st.subheader("Uses")
                        st.write(result['uses'])
                    
                    with tab3:
                        st.subheader("Side Effects")
                        st.write(result['side_effects'])
                else:
                    st.error(result)
            
            elif view_type == "Customer":
                result, success = search_customer_pov(medicine_name)
                
                if success:
                    st.success(f"✅ Found: **{result['name']}**")
                    
                    tab1, tab2, tab3, tab4 = st.tabs(["💊 Uses", "📖 How to Use", "⚠️ Side Effects", "❓ FAQs"])
                    
                    with tab1:
                        st.subheader("Uses")
                        st.write(result['uses'])
                    
                    with tab2:
                        st.subheader("How to Use")
                        st.write(result['how_to_use'])
                    
                    with tab3:
                        st.subheader("Side Effects")
                        st.write(result['side_effects'])
                    
                    with tab4:
                        st.subheader("FAQs")
                        st.write(result['faqs'])
                else:
                    st.error(result)
            
            elif view_type == "Pharmacy":
                result, success = search_pharmacy_pov(medicine_name)
                
                if success:
                    st.success(f"✅ Found: **{result['name']}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Short Composition")
                        st.info(result['short_composition'])
                        
                        st.subheader("💰 MRP")
                        st.info(result['mrp'])
                    
                    with col2:
                        st.subheader("📦 Pack Information")
                        st.info(result['pack'])
                        
                        st.subheader("🧪 Full Composition")
                        with st.expander("View Full Composition"):
                            st.write(result['full_composition'])
                else:
                    st.error(result)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Medicine Information System | Version 1.0</div>",
    unsafe_allow_html=True
)
