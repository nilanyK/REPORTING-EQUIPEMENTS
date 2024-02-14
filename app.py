import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from PIL import Image
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Get the directory where this script resides
script_directory = Path(__file__).parent

num_chunks = 9

# Define a function to read and concatenate all CSV file chunks
@st.cache(allow_output_mutation=True)
def read_and_concat_chunks():
    # Initialize an empty DataFrame to hold all chunks
    combined_df = pd.DataFrame()

    # Iterate over each CSV file chunk
    for file_index in range(1, num_chunks + 1):
        # Construct the file path for the CSV chunk
        csv_file_path = script_directory / f'data_chunk_{file_index}.csv'

        # Read the CSV chunk into a DataFrame
        chunk_df = pd.read_csv(csv_file_path)

        # Concatenate the chunk to the combined DataFrame
        combined_df = pd.concat([combined_df, chunk_df], ignore_index=True)

    return combined_df

# Call the function to read and concatenate chunks
equipements_df = read_and_concat_chunks()
# Convertir la colonne 'Code batiment' en type de données objet (str)
equipements_df['Code batiment'] = equipements_df['Code batiment'].astype(str)
equipements_df['IRSI'] = equipements_df['IRSI'].astype(str)
equipements_df['IRSI'] = equipements_df['IRSI'].str.replace('.0', '')

# Custom CSS to inject fonts and colors
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body {
    font-family: 'Montserrat', sans-serif;
}
h1 {
    color: #00573F;
    font-family: 'Montserrat', sans-serif;
    font-size: 2em;
}
h2 {
    font-family: 'Montserrat', sans-serif;
    color: #36bc7b;
    font-size: 1.5em;
}
.sidebar .sidebar-content {
    width: 250px;
    background-color: #f0f0f0;
    color: #333;
    font-family: 'Montserrat', sans-serif;
}
.sidebar .sidebar-content .sidebar-list {
    padding-top: 20px;
}
.sidebar .sidebar-content .sidebar-list .sidebar-item {
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 5px;
}
.sidebar .sidebar-content .sidebar-list .sidebar-item:hover {
    background-color: #e0e0e0;
}
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Set app title
st.title("Dashboard Equipements")

# Divide the page into two columns
col1, col2 = st.columns([1, 2])

# Display logo in the first column
with col1:
    # Construct the full path for the image file
    image_file_path = script_directory / 'LaPosteImmobilier_Logo_VersionEnLigne_RVB.png'
    image = Image.open(image_file_path)

    # Desired width for the image
    new_width = 200

    # Calculate the new height to maintain the aspect ratio
    aspect_ratio = image.height / image.width
    new_height = int(new_width * aspect_ratio)

    # Resize the image
    image = image.resize((new_width, new_height))
    # Display the image in Streamlit
    st.image(image)

# Sidebar content
with col1:
    selected_term = st.sidebar.radio("Onglets", ["Sites inactifs & Hors-Contrat", "Code Famille"])

# Main content
with col2:
    # Add a subtitle for each section
    if selected_term == "Sites inactifs & Hors-Contrat":
        st.markdown("<h2>Analyse des équipements des sites inactifs</h2>", unsafe_allow_html=True)
        analyse_equipements()
    elif selected_term == "Code Famille":
        st.markdown("<h2>Analyse par code famille</h2>", unsafe_allow_html=True)
        code_famille()
