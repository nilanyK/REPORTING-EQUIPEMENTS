import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from PIL import Image

st.set_page_config(layout="wide")

# Get the directory where this script resides
script_directory = Path(__file__).parent

num_chunks = 9

# Define a function to read and concatenate all CSV file chunks
@st.cache
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

# Custom CSS to inject fonts and colors
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body {
    font-family: 'Montserrat', sans-serif;
}
h1 {
    color: #00573F; /* Adjusted to match the color in the uploaded image */
    font-family: 'Montserrat', sans-serif;
    font-size: 3em; /* You can adjust the size if necessary */
}
h2 {
    font-family: 'Montserrat', sans-serif;
    color: #36bc7b; /* Adjusted to match the color in the uploaded image */
    font-size: 2em; /* You can adjust the size if necessary */
}
</style>
"""

# Apply custom CSS

st.markdown(custom_css, unsafe_allow_html=True)

# Construct the full path for the image file
image_file_path = script_directory / 'lpi.png'
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

# Sidebar with terms 
selected_term = st.sidebar.radio("Onglets : ", ["Analyse des équipements","Prediction & Explanation", "Information Retrieval", "QA"])

# Set app title
st.title("Dashboard Equipements")

def analyse_equipements:
    # Add a subtitle
    st.markdown("<h2>Analyse des équipements</h2>", unsafe_allow_html=True)
    
    # Filtrer les données selon les conditions spécifiées
    filtered_df = equipements_df[(equipements_df['statut_site'] == 'inactif') & (equipements_df['Libelle statut'] != 'Hors Contrat')]
    
    # Grouper par Code superviseur et compter le nombre d'équipements
    grouped_df = filtered_df.groupby('Code superviseur').size().reset_index(name='Nombre d\'équipements')
    
    # Créer l'histogramme avec Plotly
    fig = px.bar(grouped_df, x='Code superviseur', y='Nombre d\'équipements', title="Nombre d\'équipements de site inactifs dont le statut n'est pas hors contrat", labels={"Code superviseur": "Code Superviseur", "Nombre d'équipements": "Nombre d'Équipements"})
    # Modifier la mise en page du graphique
    fig.update_layout(xaxis_title="Code Superviseur", yaxis_title="Nombre d'Équipements")
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

# Call the corresponding function based on the selected term
if selected_term == "Analyse des équipements":
    analyse_equipements()

