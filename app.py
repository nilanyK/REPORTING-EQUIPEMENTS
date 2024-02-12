import streamlit as st
import pandas as pd
import requests
from io import StringIO

# New function to download a file from Google Drive directly
def download_file_from_google_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    session = requests.Session()
    response = session.get(url, allow_redirects=True)
    return StringIO(response.text)

@st.cache
def load_data_from_google_drive(file_id):
    csv_raw = download_file_from_google_drive(file_id)
    return pd.read_csv(csv_raw, sep=';')


if st.button('Load Data :'):
    file_id = '1khHggRA-DKIz4W6x2Ac1n9A0VDZ3XLAC'  # Extracted from your shared link
    equipements_df = load_data_from_google_drive(file_id)
    st.dataframe(equipements_df.head(10))
