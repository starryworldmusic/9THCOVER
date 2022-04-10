#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 13:08:39 2022

@author: starryworld
"""

#import library
import streamlit as st
import pandas as pd
import random
from PIL import Image
from streamlit_player import st_player

#top bar
st.set_page_config(page_title=("9th Must Go On cover歌錄音大賽"),page_icon=":tada:", layout="wide")

# Header
with st.container():
    st.title('9th Must Go On cover歌錄音大賽')
    left_column, right_column = st.columns(2)
    with left_column:
        img_cover1 = Image.open("website/images/cover1.jpg")
        st.image(img_cover1)
    with right_column:
        img_cover2 = Image.open("website/images/cover2.jpg")
        st.image(img_cover2)
    st.write("感謝大家一起參與「9th Must Go On cover歌錄音大賽」的評審工作，每次你會聽到兩首參賽作品，請投選你認為表現更佳的作品，每天最多可以投票10次。")
    st.write("勝出者可以獲豐富獎品包括：Planet Beyond時尚藍牙耳機(價值：$1580）及獎狀乙張")
    st.write("投票觀眾亦有機會獲得星格學卷$100，共會抽5名幸運員 ")
    
    