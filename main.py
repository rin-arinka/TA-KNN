import streamlit as st
from landing import *
from search import *
from PIL import Image

st.set_page_config(layout="wide")
# st.session_state.update(st.session_state)

if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Landing'
    # st.session_state.Search = ''

def CB_Landing():
    st.session_state.active_page = 'Landing'
def CB_Search():
    st.session_state.active_page = 'Search'
icon = Image.open('img/icon.png')
st.image(icon, width=150)
st.write('---')
print (st.session_state)
if st.session_state.active_page == 'Landing':
    CB_Landing()
    landing()
elif st.session_state.active_page == 'Search':
    CB_Search()
    search()