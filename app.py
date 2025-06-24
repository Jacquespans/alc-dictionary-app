import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('alc-dictionary-credentials.json', scopes=scope)
client = gspread.authorize(credentials)

# Open the main sheet (definitions) and the submissions sheet
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1B_09WvM16z_jJ8HAZxu-v09AZCm5-5gmVmBjX4qznK8/edit?usp=sharing")
definitions_sheet = spreadsheet.sheet1
submissions_sheet = spreadsheet.worksheet("Submissions")

# Load data into a DataFrame
data = pd.DataFrame(definitions_sheet.get_all_records())

# Streamlit app
st.set_page_config(page_title="ALC Dictionary", layout="centered")
st.title("📘 ALC Dictionary")

# Search bar
query = st.text_input("Search for a term:")
if query:
    results = data[data['Term'].str.contains(query, case=False, na=False)]
    if not results.empty:
        for i, row in results.iterrows():
            st.markdown(f"**{row['Term']}**: {row['Definition']}")
    else:
        st.info("No matching term found.")

st.markdown("---")
st.header("📬 Submit a New Term")

with st.form("submission_form"):
    name = st.text_input("Your Name")
    new_term = st.text_input("Term")
    new_definition = st.text_area("Definition")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and new_term and new_definition:
            submissions_sheet.append_row([name, new_term, new_definition])
            st.success("Your term has been submitted!")
        else:
            st.error("Please fill in all fields.")
