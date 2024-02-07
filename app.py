import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from pathlib import Path

# Get the directory where the script is located
script_directory = Path(__file__).parent

# Function to load data from CSV files
def load_csv(file_name):
    # Construct the full path for the CSV file
    file_path = script_directory / file_name
    # Read the CSV file using the full path
    return pd.read_csv(file_path, sep=';')

# Function to load data from Excel files
def load_excel(file_name):
    # Construct the full path for the Excel file
    file_path = script_directory / file_name
    # Read the Excel file using the full path
    return pd.read_excel(file_path)

# Chargement des données

uploaded_file = st.file_uploader("Upload du fichier CSV", type=['csv'])
if uploaded_file is not None:
    equipements_df = pd.read_csv(uploaded_file, sep=';')
   

mapping_df = load_excel('Jointure attributs code famille.xlsx')
map = load_excel('IRSI_statut.XLSX')

map['IRSI'] = map['IRSI'].astype(str).str.split('.').str[0]
map = dict(zip(map.IRSI, map.statut))
equipements_df['statut_site'] = equipements_df['IRSI'].map(map)

# Fonction pour filtrer les données
def filter_data(code_superviseur, code_famille):
    # Filtrer les données par code superviseur
    filtered_by_sup = equipements_df[equipements_df['Code superviseur'] == code_superviseur]
    
    # Filtrer les données par code famille
    filtered_by_fam = filtered_by_sup[filtered_by_sup['Code famille'] == code_famille]
    
    return filtered_by_fam

# Sidebar
st.sidebar.header('Sélectionnez vos options')
code_superviseur = st.sidebar.selectbox('Code superviseur', equipements_df['Code superviseur'].unique())
code_famille = st.sidebar.selectbox('Code famille', equipements_df['Code famille'].unique())

# Filtrer les données
filtered_data = filter_data(code_superviseur, code_famille)

# Affichage de l'histogramme
st.subheader('Nombre d\'équipements de site inactifs dont le statut n\'est pas hors contrat')
fig_hist = px.histogram(filtered_data, x='Code superviseur', title='Nombre d\'équipements inactifs par superviseur')
st.plotly_chart(fig_hist)

# Affichage de la liste des équipements
st.subheader('Liste des équipements')
columns_to_display = ['1', '2', '3', '4', '7', '8', '9', '10', '13', '20']  # Correspondant à A, B, C, D, G, H, I, J, M, T
st.write(filtered_data[columns_to_display])

# Affichage des pie charts
st.subheader('Pourcentage de valeurs renseignées pour chaque attribut')
figs = []
for attribut in mapping_df['attribut 1'].values:
    non_null_count = filtered_data[attribut].notna().sum()
    total_count = len(filtered_data)
    renseigne_percentage = (non_null_count / total_count) * 100
    non_renseigne_percentage = 100 - renseigne_percentage
    labels = ['Renseigné', 'Non renseigné']
    values = [renseigne_percentage, non_renseigne_percentage]
    colors = ['#9acd32', '#ff7f0e']  # Vert pastel clair pour les valeurs renseignées, Rouge pastel clair pour les valeurs non renseignées
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig.update_layout(title=f'Pourcentage de valeurs renseignées pour l\'attribut {attribut}')
    figs.append(fig)

# Affichage des graphiques
for fig in figs:
    st.plotly_chart(fig)
