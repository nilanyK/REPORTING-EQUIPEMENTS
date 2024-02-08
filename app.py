import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from pathlib import Path

# Get the directory where the script is located
script_directory = Path(__file__).parent

# Function to load data from CSV files
@st.cache
def load_csv(file_name):
    # Construct the full path for the CSV file
    file_path = script_directory / file_name
    # Read the CSV file using the full path
    return pd.read_csv(file_path, sep=';')

# Function to load data from Excel files
@st.cache
def load_excel(file_name):
    # Construct the full path for the Excel file
    file_path = script_directory / file_name
    # Read the Excel file using the full path
    return pd.read_excel(file_path)

# Chargement des données
uploaded_file = st.file_uploader("Upload du fichier CSV", type=['csv'])
if uploaded_file is not None:
    equipements_df = pd.read_csv(uploaded_file, sep=';')
    st.write(equipements_df)
    
    

    
   
    
  
