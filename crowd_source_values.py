import streamlit as st
from streamlit import session_state as ss
from streamlit_gsheets import GSheetsConnection 
import pandas as pd
import numpy as np
from pyfonts import set_default_font, load_google_font
from PIL import Image
import urllib

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
    game_line = pd.read_parquet('starter_games.parquet').iloc[index].round(2)
    return game_line
    
game_line = load_game(ss['index'])

ip_adj = int(game_line['IP'])+(game_line['IP'] - int(game_line['IP']))*3/10
earned_runs = int(game_line['ER'])
hits = int(game_line['H'])
hit_text = f'{hits} Hits' if hits!=1 else f'{hits} Hit'

temp_text = []
for stat in ['2B','3B','HR']:
    stat_val = int(game_line[stat])
    if stat_val>0:
        temp_text += [f'{stat_val} {stat}']
xbh_text = '' if int(sum(game_line[['2B','3B','HR']]))==0 else ' ('+', '.join(temp_text)+')'

walks = int(game_line['BB'])
walk_text = f'{walks} BBs' if walks!=1 else f'{walks} BB'

strikeouts = int(game_line['SO'])
strikeout_text = f'{strikeouts} Ks' if strikeouts!=1 else f'{strikeouts} K'

era = game_line['ERA']
whip = game_line['WHIP']

game_line_text = f'{ip_adj:.1f} IP, {earned_runs} ER, {hit_text}{xbh_text}, {walk_text}, {strikeout_text}<br>{era:.2f} ERA, {whip:.2f} WHIP'

start_label = f'<p style="color:{pl_text}; text-align: center; font-weight: bold; font-size: 24px;">Start Results</p>'
st.markdown(start_label, unsafe_allow_html=True)

game_line_text = f'<p style="color:w; text-align: center; font-weight: bold; font-size: 20px;">{game_line_text}</p>'
st.markdown(game_line_text, unsafe_allow_html=True)

input_label = f'<p style="color:{pl_text}; text-align: center; font-weight: bold; font-size: 20px;">What grade would you give that start?</p>'
st.markdown(input_label, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3,width=1000,gap=None)
with col2:
    game_grade = st.pills('',
                          # ['F','D-','D','D+','C-','C','C+','B-','B','B+','A-','A','A+'],
                          ['A-','A','A+','B-','B','B+','C-','C','C+','D-','D','D+','F'],
                          width=160,
                          default='C'
                          )
col1, col2, col3 = st.columns([0.375,0.325,0.3])
with col2:
    if st.button("Submit Grade"):
        game_line = pd.DataFrame(game_line).T
        game_line['Grade'] = game_grade
        grade_df = conn.read(
            worksheet="Responses",
            ttl="10m"
        )
        game_line = conn.update(
          worksheet="Responses",
          data=pd.concat([grade_df,
                          game_line.reset_index(names='game_id')],
                         ignore_index=True),
          )
        st.cache_data.clear()
        del st.session_state['index']
        st.rerun()
