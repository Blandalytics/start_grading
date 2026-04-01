import streamlit as st
from streamlit import session_state as ss
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

if 'index' not in ss:
    ss['index'] = np.random.randint(0,19031)

def load_game(index):
    game_line = pd.read_parquet('starter_games.parquet').iloc[[index]].round(2)
    return game_line
    
game_line = load_game(ss['index'])

start_label = f'<p style="color:{pl_text}; text-align: center; font-weight: bold; font-size: 24px;">Start Results</p>'
st.markdown(start_label, unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.3,0.4,0.3])

with col2:
    first_df = (
        game_line[game_line.columns.values[:6]]
        .astype('str')
        .style
        .hide(axis="index")
        .set_properties(**{'text-align': 'center'})
        .set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    )

    # Display using markdown
    st.markdown(first_df.to_html(), unsafe_allow_html=True)
    
    second_df = (
        game_line[game_line.columns.values[6:]]
        .astype('str')
        .style
        .hide(axis="index")
        .set_properties(**{'text-align': 'center'})
        .set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    )

    # Display using markdown
    st.markdown(second_df.to_html(), unsafe_allow_html=True)
    # st.dataframe(game_line[game_line.columns.values[:6]],hide_index=True)
    # st.dataframe(game_line[game_line.columns.values[6:]],hide_index=True)

slider_label = f'<p style="color:{pl_text}; text-align: center; font-weight: bold; font-size: 20px;">How good was that Start?<br>(1 = Terrible, 3 = Average, 5 = Amazing)</p>'
st.markdown(slider_label, unsafe_allow_html=True)
game_score = st.slider('',
                       min_value=1, 
                       max_value=5,
                       value=3)

if st.button("Submit Score"):
    game_line['Score'] = game_score
    score_df = conn.read(
        worksheet="Responses",
        ttl="10m"
    )
    game_line = conn.update(
      worksheet="Responses",
      data=pd.concat([score_df,
                      game_line.reset_index(names='game_id')],
                     ignore_index=True),
      )
    st.cache_data.clear()
    del st.session_state['index']
    st.rerun()
