import streamlit as st
from streamlit_gsheets import GSheetsConnection 
import polars as pl
import numpy as np
from pyfonts import set_default_font, load_google_font

sheet_url = 'https://docs.google.com/spreadsheets/d/14oyLIXsnDM4IZqGAca7mk5831_1WnxG2WEoSoILo5mg/edit?usp=sharing'

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

game_line = pl.read_parquet('starter_games.parquet').sample()

game_score = st.slider('Start Score',min_value=1, max_value=7,value=4)

st.button("Submit", type="primary")
if st.button("Submit Score"):
    game_line = game_line.with_columns(pl.lit(game_score).alias("Score"))
    game_line = conn.update(
      worksheet="Responses",
      data=game_line,
      )
    st.cache_data.clear()
    st.rerun()
