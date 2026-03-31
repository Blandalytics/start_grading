import streamlit as st
from streamlit_gsheets import GSheetsConnection 
import pandas as pd
import numpy as np
from pyfonts import set_default_font, load_google_font

pl_white = '#FFFFFF'
pl_background = '#292C42'
pl_text = '#00D4FF'#'#72CBFD'
pl_line_color = '#8D96B3'
pl_highlight = '#F1C647'

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def load_game():
    return pd.read_parquet('starter_games.parquet').sample().round(2)
game_line = load_game()
st.dataframe(game_line,hide_index=True)

slider_label = f'<p style="color:{pl_text}; font-weight: bold; font-size: 24px;">Start Score (1 = Terrible, 4 = Average, 7 = Amazing)</p>'
st.markdown(slider_label, unsafe_allow_html=True)
game_score = st.slider('',
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
