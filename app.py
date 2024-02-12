import streamlit as st
from PIL import Image
from pathlib import Path

# Define the directory where this script resides
script_directory = Path(__file__).parent

# Custom CSS to inject fonts and colors
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body {
    font-family: 'Montserrat', sans-serif;
}
h1 {
    color: #4CAF50; /* Adjusted to match the color in the uploaded image */
    font-family: 'Montserrat', sans-serif;
    font-size: 3em; /* You can adjust the size if necessary */
}
h2 {
    font-family: 'Montserrat', sans-serif;
    color: #1976D2; /* Adjusted to match the color in the uploaded image */
    font-size: 2em; /* You can adjust the size if necessary */
}
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Load the image
image_path = script_directory / 'lpi.png' # Make sure to use the correct file name
image = Image.open(image_path)

# Resize the image if needed (this example resizes to 200x200)
# You can adjust the size as needed
image = image.resize((200, 200))

# Display the image in Streamlit using the PIL Image object
# Removed use_column_width to use the actual size of the image
st.image(image)

# Set app title
st.title("Dashboard Equipements")

# Add a subtitle
st.markdown("<h2>Analyse des équipements</h2>", unsafe_allow_html=True)

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
