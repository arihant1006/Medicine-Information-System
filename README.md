# Medicine Information System

A comprehensive medicine information lookup system built with Python and Streamlit, providing tailored information for customers, pharmacies, and doctors.

## Features

- Multi-View Interface: Three different perspectives (Customer, Pharmacy, Doctor)
- Smart Search: Autocomplete search with 280,000+ medicines
- Responsive Design: Works on desktop and mobile devices
- Fast Lookup: Binary search algorithm for quick results

## User Views

### Customer View
- Medicine uses and benefits
- How to use instructions
- Side effects information
- Frequently asked questions (FAQs)

### Pharmacy View
- Medicine composition (short & full)
- MRP and pricing information
- Pack details and specifications

### Doctor View
- Complete composition details
- Medical uses and indications
- Side effects and contraindications

## Technology Stack

- Python 3.10
- Streamlit - Web UI framework
- Pandas - Data processing
- CSV - Data storage format

## Project Structure
```
medicine-info-system/
├── ui.py                 # Main Streamlit application
├── CustomerPOV.py        # Customer view logic
├── DoctorPOV.py          # Doctor view logic
├── PharmacyPOV.py        # Pharmacy view logic
├── Data/                 # Medicine database (not included)
│   ├── A/
│   │   └── A_medicines.csv
│   ├── B/
│   │   └── B_medicines.csv
│   └── ...
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Miniconda/Anaconda (recommended)

### Setup

1. Clone the repository
```bash
git clone https://github.com/arihant1006/medicine-info-system.git
cd medicine-info-system
```

2. Create conda environment
```bash
conda create -n medicine_project python=3.10 -y
conda activate medicine_project
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add your medicine database
   - Place CSV files in Data/ folder organized by first letter
   - Format: Data/A/A_medicines.csv, Data/B/B_medicines.csv, etc.

## Usage

1. Activate the environment
```bash
conda activate medicine_project
```

2. Run the application
```bash
streamlit run ui.py
```

3. Access the app
   - Open browser and navigate to http://localhost:8501
   - Select your view type (Customer/Pharmacy/Doctor)
   - Search for medicines using the autocomplete search

## Data Format

The system expects CSV files with the following columns:
- title - Medicine name
- shortComposition - Brief composition
- composition - Full composition details
- uses - Medical uses
- howToUse - Usage instructions
- sideEffects - Side effects information
- faqs - Frequently asked questions
- mrp - Maximum retail price
- price - Selling price
- pack - Packaging information

## Motivation

Built to provide accessible and organized medicine information to different stakeholders in the healthcare ecosystem - making medical information more accessible to everyone.

## License

MIT License - feel free to use this project for learning and development.

## Author

Arihant
- GitHub: @arihant1006
- Email: ch1240578@iitd.ac.in

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## Disclaimer

This is an educational project. Always consult healthcare professionals for medical advice.
