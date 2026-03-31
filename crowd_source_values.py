import streamlit as st
from streamlit_gsheets import GSheetsConnection 
from pyfonts import set_default_font, load_google_font

sheet_url = 'https://docs.google.com/spreadsheets/d/14oyLIXsnDM4IZqGAca7mk5831_1WnxG2WEoSoILo5mg/edit?usp=sharing'

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=sheet_url)

st.dataframe(df,hide_index=True)
