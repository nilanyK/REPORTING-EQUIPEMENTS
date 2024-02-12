import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

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

# Filtrer les données selon les conditions spécifiées
filtered_df = equipements_df[(equipements_df['statut_site'] == 'inactif') & (equipements_df['Libelle statut'] != 'Hors Contrat')]

# Grouper par Code superviseur et compter le nombre d'équipements
grouped_df = filtered_df.groupby('Code superviseur').size().reset_index(name='Nombre d\'équipements')

# Créer l'histogramme avec Plotly
fig = px.bar(grouped_df, x='Code superviseur', y='Nombre d\'équipements', title="Nombre d\'équipements de site inactifs dont le statut n'est pas hors contrat")
# Afficher le graphique dans Streamlit
st.plotly_chart(fig)
