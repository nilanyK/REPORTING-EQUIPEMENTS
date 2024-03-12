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
    color: #00573F; /* Adjusted to match the color in the uploaded image */
    font-family: 'Montserrat', sans-serif;
    font-size: 2em; /* You can adjust the size if necessary */
}
h2 {
    font-family: 'Montserrat', sans-serif;
    color: #36bc7b; /* Adjusted to match the color in the uploaded image */
    font-size: 1em; /* You can adjust the size if necessary */
}
/* Largeur de la barre latérale */
.sidebar .sidebar-content {
            width: 300px;
            background-color: #36bc7b;
            color: white;
            font-family: 'Montserrat', sans-serif;
}
/* Style des onglets */
.sidebar .sidebar-content .sidebar-list {
            padding-top: 20px;
}
.sidebar .sidebar-content .sidebar-list .sidebar-item {
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
}
.sidebar .sidebar-content .sidebar-list .sidebar-item:hover {
background-color: #2c8e5d;
        }
</style>
"""

# Apply custom CSS

st.markdown(custom_css, unsafe_allow_html=True)


#mapping_dict_path = script_directory / 'mapping_dict.json'
# Lire le dictionnaire depuis le fichier JSON
with open('mapping_dict.json', 'r') as f:
    mapping_dict = json.load(f)

with open('mapping_lot_dict.json', 'r') as f:
    mapping_dict_lot = json.load(f)

with open('mapping_MTK.json', 'r') as f:
    mapping_mtk_dict = json.load(f)


equipements_df['MTK'] = equipements_df['Code superviseur'].map(mapping_mtk_dict)

equipements_df['Lot'] = equipements_df['Code superviseur'].map(mapping_dict_lot)


    
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

# Contenu de la barre latérale avec des onglets
selected_term = st.sidebar.radio("Onglets",["Sites inactifs & Hors-Contrat","Code Famille"])

# Set app title
st.title("Reporting Équipements")

def analyse_equipements():
    # Add a subtitle
    st.markdown("<h2>Analyse des équipements de site inactifs dont le statut n'est pas hors contrat</h2>", unsafe_allow_html=True)
    
    # Filtrer les données selon les conditions spécifiées
    filtered_df = equipements_df[(equipements_df['statut_site'] == 'inactif') & (equipements_df['Libelle statut'] != 'Hors Contrat')]
    
    # Grouper par Code superviseur et compter le nombre d'équipements
    grouped_df = filtered_df.groupby('Code superviseur').size().reset_index(name='Nombre d\'équipements')
    
    # Créer l'histogramme avec Plotly pour le graphique fig1
    fig1 = px.bar(grouped_df, x='Code superviseur', y='Nombre d\'équipements', title="Code Superviseur", labels={"Code superviseur": "Code Superviseur", "Nombre d'équipements": "Nombre d'Équipements"}, color_discrete_sequence=['#00573F'])

    
    # Modifier la mise en page du graphique fig1
    fig1.update_layout(xaxis_title="Code Superviseur", yaxis_title="Nombre d'Équipements")
    
    # Calculate the number of inactifs_hors_contrat and inactifs_non_hors_contrat
    inactifs_hors_contrat = equipements_df[(equipements_df['statut_site'] == 'inactif') & (equipements_df['Libelle statut'] == 'Hors Contrat')].shape[0]
    inactifs_non_hors_contrat = equipements_df[(equipements_df['statut_site'] == 'inactif') & (equipements_df['Libelle statut'] != 'Hors Contrat')].shape[0]
    
    # Données pour le camembert
    labels = ['Inactifs - Hors Contrat', 'Inactifs - Non Hors Contrat']
    values = [inactifs_hors_contrat, inactifs_non_hors_contrat]
    
    # Création du camembert avec Plotly
    fig2 = px.pie(names=labels, values=values, title="Répartition des Équipements des Sites Inactifs", color_discrete_sequence=['#00573F', '#36bc7b'])
    

    # Afficher les histogrammes côte à côte dans deux colonnes
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    
    # Vous pouvez également modifier les couleurs du tableau interactif si nécessaire
    # Sélection des colonnes spécifiques par leur indice
    colonnes_a_afficher = [0, 1, 2, 3, 6, 7, 8, 9, 12, 19]

    # Sélection des colonnes spécifiques par leur indice
    df_filtered_columns = filtered_df.iloc[:, colonnes_a_afficher]
    # Création d'un tableau interactif
    st.write("Liste des Équipements de sites inactifs non Hors Contrat")
    st.dataframe(df_filtered_columns.reset_index(drop=True))


def code_famille():
    # Add a subtitle
    st.markdown("<h2>Analyse par code famille</h2>", unsafe_allow_html=True)
    # Créer un menu déroulant  pour choisir le code famille
    code_famille_test = st.selectbox("Choisissez un code famille :", list(mapping_dict.keys()))
    
    # Sélectionner les attributs correspondant au code famille testé
    attributs_test = mapping_dict[code_famille_test]
    
    # Filtrer les données du DataFrame sur le code famille sélectionné
    equipements_famille = equipements_df[equipements_df['Code famille'] == code_famille_test]

    # Filtrer par Lot (si l'utilisateur le souhaite)
    if st.checkbox("Filtrer par Lot"):
        lot_options = equipements_famille['Lot'].unique().tolist()
        lot_selected = st.selectbox("Choisissez un Lot :", [''] + lot_options)
        if lot_selected:
            equipements_famille = equipements_famille[equipements_famille['Lot'] == lot_selected]
    
    # Filtrer par MTK (si l'utilisateur le souhaite)
    if st.checkbox("Filtrer par MTK"):
        mtk_options = equipements_famille['MTK'].unique().tolist()
        mtk_selected = st.selectbox("Choisissez un MTK :", [''] + mtk_options)
        if mtk_selected:
            equipements_famille = equipements_famille[equipements_famille['MTK'] == mtk_selected]

    # Filtrer par Libelle statut (si l'utilisateur le souhaite)
    if st.checkbox("Filtrer par Libelle statut"):
        libelle_statut_options = equipements_famille['Libelle statut'].unique().tolist()
        libelle_statut_selected = st.selectbox("Choisissez un Libelle statut :", [''] + libelle_statut_options)
        if libelle_statut_selected:
            equipements_famille = equipements_famille[equipements_famille['Libelle statut'] == libelle_statut_selected]
"""
    # Filtrer par Equipement réglementaire (si l'utilisateur le souhaite)
    if st.checkbox("Filtrer par Equipement réglementaire"):
        equipement_reglementaire_options = equipements_famille['Equipement rÃ¨glementaire'].unique().tolist()
        equipement_reglementaire_selected = st.selectbox("Choisissez un Equipement réglementaire :", [''] + equipement_reglementaire_options)
        if equipement_reglementaire_selected:
            equipements_famille = equipements_famille[equipements_famille['Equipement rÃ¨glementaire'] == equipement_reglementaire_selected]
"""
    # Filtrer par Niveau Equipement1 (si l'utilisateur le souhaite)
    if st.checkbox("Filtrer par Niveau Equipement1"):
        niveau_equipement1_options = equipements_famille['Niveau Equipement1'].unique().tolist()
        niveau_equipement1_selected = st.selectbox("Choisissez un Niveau Equipement1 :", [''] + niveau_equipement1_options)
        if niveau_equipement1_selected:
            equipements_famille = equipements_famille[equipements_famille['Niveau Equipement1'] == niveau_equipement1_selected]
    
    # Sélectionner les colonnes spécifiées par leur index
    colonnes_indices = [0, 1, 2, 3, 6, 7, 8, 9, 12, 19]  # Index des colonnes A, B, C, D, G, H, I, J, M, T
    equipements_famille_selected = equipements_famille.iloc[:, colonnes_indices]
    
    # Afficher les colonnes spécifiées
    st.dataframe(equipements_famille_selected.reset_index(drop=True))
    
    colors = ['#36bc7b','#00573F']

    # Créer une liste pour les noms des attributs et une autre pour le nombre de données non nulles correspondant à chaque attribut
    attributs_names = []
    non_null_counts = []
    total_counts = []
    
    # Parcourir les attributs pour compter les données non nulles et le nombre total de données
    for attribut in attributs_test:
        attributs_names.append(attribut)
        non_null_count = equipements_famille[attribut].notna().sum()
        total_count = len(equipements_famille)
        non_null_counts.append(non_null_count)
        total_counts.append(total_count)
    

    fig = go.Figure()
    fig.add_trace(go.Bar(x=attributs_names, y=non_null_counts, name='Renseigné', marker_color='#36bc7b'))
    fig.add_trace(go.Bar(x=attributs_names, y=[total - non_null for total, non_null in zip(total_counts, non_null_counts)], name='Non renseigné', marker_color='#00573F'))
    
    # Ajouter des informations sur l'axe x et y ainsi que le titre du graphique
    fig.update_xaxes(title_text='Attributs')
    fig.update_yaxes(title_text='Nombre de valeurs')
    fig.update_layout(title='Nombre de données renseignées pour le code famille {}'.format(code_famille_test),
                      barmode='stack')
    
    st.plotly_chart(fig)
    
    # Créer un pie chart pour chaque attribut avec Plotly
    st.markdown("<h2>Pourcentage de valeurs renseignées par attribut</h2>", unsafe_allow_html=True)
    for attribut, non_null_count in zip(attributs_test, non_null_counts):
        renseigne_percentage = (non_null_count / len(equipements_famille)) * 100
        non_renseigne_percentage = 100 - renseigne_percentage
        labels = ['Renseigné', 'Non renseigné']
        values = [renseigne_percentage, non_renseigne_percentage]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
        fig.update_layout(title='Pourcentage de valeurs renseignées pour l\'attribut {}'.format(attribut))
        st.plotly_chart(fig)





# Call the corresponding function based on the selected term
if selected_term == "Sites inactifs & Hors-Contrat":
    analyse_equipements()
elif selected_term == "Code Famille":
    code_famille()
