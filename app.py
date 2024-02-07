import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Chargement des données
equipements_df = pd.read_csv('Liste des equipement.csv', sep=";")
mapping_df = pd.read_excel('Jointure attributs code famille.xlsx')

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
columns_to_display = ['A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 'M', 'T']
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
