import streamlit as st
from streamlit_gsheets import GSheetsConnection 
import pandas as pd
import numpy as np
from pyfonts import set_default_font, load_google_font

# sheet_url = 'https://docs.google.com/spreadsheets/d/14oyLIXsnDM4IZqGAca7mk5831_1WnxG2WEoSoILo5mg/edit?usp=sharing'

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def load_game():
    return pd.read_parquet('starter_games.parquet').sample().round(2)
game_line = load_game()
st.dataframe(game_line,hide_index=True)

slider_label = f'<p style="color:{pl_text}; font-weight: bold; font-size: 24px;">Start Score (1 = Terrible, 4 = Average, 7 = Amazing)</p>'
st.markdown(slider_label, unsafe_allow_html=True)
game_score = st.slider(#'Start Score (1 = Terrible, 4 = Average, 7 = Amazing)',
                       min_value=1, 
                       max_value=7,
                       value=4)

if st.button("Submit Score"):
    game_line['Score'] = game_score
    score_df = conn.read(
        worksheet="Responses",
        ttl="10m"
    )
    game_line = conn.update(
      worksheet="Responses",
      data=pd.concat([score_df,
                      game_line],
                     ignore_index=True),
      )
    st.cache_data.clear()
    st.rerun()
