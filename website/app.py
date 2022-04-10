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
import datetime
from PIL import Image


#intial session state
if 'admited' not in st.session_state:
    st.session_state['admited'] = 0
if 'repeatvote' not in st.session_state:
    st.session_state['repeatvote'] = 0
if 'votesong' not in st.session_state:
    st.session_state['votesong'] = ""
if 'song1' not in st.session_state:
    st.session_state['song1'] = ""
if 'song2' not in st.session_state:
    st.session_state['song2'] = ""
if 'r1' not in st.session_state:
    st.session_state['r1'] = random.randint(0,9)
if 'r2' not in st.session_state:
    st.session_state['r2'] = random.randint(0,9)
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'remain' not in st.session_state:
    st.session_state['remain'] = 10
if 'number' not in st.session_state:
    st.session_state['number'] = 88888888
while st.session_state['r1'] == st.session_state['r2']:
    st.session_state['r1'] = random.randint(0,9)

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
    
#date process  
time = datetime.datetime.now()
today = str(time.strftime("%Y"+"-"+"%m"+"-"+"%d"))
number_df = pd.read_csv('website/number.csv', sep=',',index_col="number")
df = pd.read_csv('website/data.csv', sep=',')

def voting():
    if st.session_state['counter'] >= 10:
        st.error(str(st.session_state['number'])+"的使用者你好，今日你已經完成了所有投票，明天可以繼續。") 
        st.session_state['admited'] = 0
    elif st.session_state['counter'] <10:
        st.info(str(st.session_state['number'])+"的使用者你好，今日你已經投了"+ str(st.session_state['counter']) +"次投票，你今天最多可多投"+str(st.session_state['remain'])+"次投票")                 
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Song1 - "+df.iloc[st.session_state['r1'],4])
            st_player(df.iloc[st.session_state['r1'],1])
            
        with right_column:
            st.header("Song2 - "+df.iloc[st.session_state['r2'],4])
            st_player(df.iloc[st.session_state['r2'],1])
        st.session_state['song1'] = str("Song1 - "+df.iloc[st.session_state['r1'],4])
        st.session_state['song2'] = str("Song2 - "+df.iloc[st.session_state['r2'],4])
        song = [st.session_state['song1'],st.session_state['song2']]
        st.session_state['votesong'] = st.radio('請投選你認為表現更佳的作品',song,key='vote_radio')    
        st.button("投票",on_click=voted)


def voted():
    st.session_state['repeatvote'] = 1
    if st.session_state['vote_radio'] == st.session_state['song1']:
        df.iloc[st.session_state['r1'],5] += 1
        df.to_csv("website/data.csv", index=False)
        number_df.loc[st.session_state['number'],today] += 1
        number_df.to_csv("website/number.csv")
        st.session_state['counter'] = int(number_df.loc[st.session_state['number'],today])
        st.session_state['remain']  = 10 - st.session_state['counter']
    elif st.session_state['vote_radio'] == st.session_state['song2']:
        df.iloc[st.session_state['r2'],5] += 1
        df.to_csv("website/data.csv", index=False)
        st.session_state['check_submit'] = 0
        number_df.loc[st.session_state['number'],today] += 1
        number_df.to_csv("website/number.csv")
        st.session_state['counter'] = int(number_df.loc[st.session_state['number'],today])
        st.session_state['remain']  = 10 - st.session_state['counter']

def refesh():
    st.session_state['repeatvote'] = 0
    st.session_state['r1'] = random.randint(0,9)
    st.session_state['r2'] = random.randint(0,9)
    while st.session_state['r1'] == st.session_state['r2']:
        st.session_state['r1'] = random.randint(0,9)
    voting()
    
with st.container():
    with st.form(key="checknumber"):
        number = st.text_input("請輸入你的電話號碼")
        num_submitted = st.form_submit_button("提交")
        
if num_submitted:
    st.session_state['number'] = int(number)
    if st.session_state['number'] in number_df.index:
        st.session_state['counter'] = int(number_df.loc[st.session_state['number'],today])
        st.session_state['admited'] = 1
        st.session_state['remain']  = 10 - st.session_state['counter']
        if st.session_state['counter'] >= 10:
            st.error(str(number)+"的使用者你好，今日你已經完成了所有投票，明天可以繼續。")  
            st.session_state['admited'] = 0
    else:
        st.error("你輸入的電話"+number+"未有登記，如需登記請whatsapp 61776662")

     
if st.session_state['admited'] == 1:
    if st.session_state['repeatvote'] == 0:
        voting()
    elif st.session_state['repeatvote'] == 1:
        with st.container():
            st.success('你成功投左'+st.session_state['votesong']+'一票')
            left_column, right_column = st.columns(2)
            with left_column:
                st.write("剛才song1 - "+df.iloc[st.session_state['r1'],4]+"的演唱歌手是"+df.iloc[st.session_state['r1'],3])
                img1 = Image.open("website/images/"+df.iloc[st.session_state['r1'],2])
                st.image(img1)
            with right_column:
                st.write("剛才song2 - "+df.iloc[st.session_state['r2'],4]+"的演唱歌手是"+df.iloc[st.session_state['r2'],3])
                img2 = Image.open("website/images/"+df.iloc[st.session_state['r2'],2])
                st.image(img2)
            st.button(label="更新下一組歌曲",on_click=refesh)
                
