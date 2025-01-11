# from knnclass import KNN_Classifier
# import pandas as pd

# list_klasifikasi_caption = KNN_Classifier.train_caption_classifier('bundatraveler')
# print (len(list_klasifikasi_caption))
from curses import window
from bokeh.models.widgets import Div
import streamlit as st
klik = st.button(st.image('img/_kakituli.jpg', width = 200))
if klik:
    js = window.open('https://www.streamlit.io/')
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)