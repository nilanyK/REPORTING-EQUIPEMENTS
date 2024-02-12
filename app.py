import streamlit as st
import pandas as pd
import gdown

# Function to download the CSV file from Google Drive
@st.cache
def download_file_from_google_drive(file_id, output_file):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output_file, quiet=False)

# Function to read the CSV file
def read_csv_file(file_path):
    return pd.read_csv(file_path)

st.title('CSV File Reader from Google Drive')

    # Input field to enter Google Drive file ID
file_id = st.text_input('Enter Google Drive File ID:')

if file_id:
    try:
        # Download the file
        st.info("Downloading file from Google Drive...")
        file_path = 'Liste des equipement.csv'  # You can change the name here if needed
        download_file_from_google_drive("1khHggRA-DKIz4W6x2Ac1n9A0VDZ3XLAC", file_path)
            
        # Read the CSV file
        st.success("File downloaded successfully!")
        st.info("Reading CSV file...")
        df = read_csv_file(file_path)
            
        # Display the DataFrame
        st.write(df)
    except Exception as e:
        st.error(f"Error: {e}")

