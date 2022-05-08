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
from streamlit_player import st_player
from supabase import create_client, Client

#top bar
st.set_page_config(page_title=("Cover 比賽"),page_icon=":microphone:", layout="wide")

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

#intial session state
if 'admited' not in st.session_state:
    st.session_state['admited'] = 0
if 'repeatvote' not in st.session_state:
    st.session_state['repeatvote'] = 0
if 'nowvote' not in st.session_state:
    st.session_state['nowvote'] = 0
if 'newcount' not in st.session_state:
    st.session_state['newcount'] = 0
if 'votesong' not in st.session_state:
    st.session_state['votesong'] = ""
if 'song1' not in st.session_state:
    st.session_state['song1'] = ""
if 'song2' not in st.session_state:
    st.session_state['song2'] = ""
if 'r1' not in st.session_state:
    st.session_state['r1'] = random.randint(1,19)
if 'r2' not in st.session_state:
    st.session_state['r2'] = random.randint(1,19)
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'remain' not in st.session_state:
    st.session_state['remain'] = 10
if 'number' not in st.session_state:
    st.session_state['number'] = 88888888
while st.session_state['r1'] == st.session_state['r2']:
    st.session_state['r1'] = random.randint(1,10)

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
    st.write("投票觀眾亦有機會獲得星格學卷$100，共會抽5名幸運兒 ")
    
#date process  
datasql = supabase.table("data").select("*").execute()
numbersql = supabase.table("number").select("*").execute()
df = pd.DataFrame(datasql.data).set_index("id")
number_df = pd.DataFrame(numbersql.data).set_index("number")
time = datetime.datetime.now()
today = str(time.strftime("%Y"+"-"+"%m"+"-"+"%d"))

def updatevote1():
    datasql = supabase.table("data").select("*").execute()
    df = pd.DataFrame(datasql.data).set_index("id")
    st.session_state['nowvote'] = df.loc[st.session_state['r1'],"vote"]
    st.session_state['nowvote'] += 1
    new1 = int(st.session_state['nowvote'])
    rr1 = int(st.session_state['r1'])
    supabase.table("data").update({"vote":new1}).eq("id",rr1).execute()
    
def updatevote2():
    datasql = supabase.table("data").select("*").execute()
    df = pd.DataFrame(datasql.data).set_index("id")
    st.session_state['nowvote'] = df.loc[st.session_state['r2'],"vote"]
    st.session_state['nowvote'] += 1
    new2 = int(st.session_state['nowvote'])
    rr2 = int(st.session_state['r2'])
    supabase.table("data").update({"vote":new2}).eq("id",rr2).execute()
    
def updatecount():
    numbersql = supabase.table("number").select("*").execute()
    number_df = pd.DataFrame(data = numbersql.data).set_index("number")
    st.session_state['newcount'] = number_df.loc[st.session_state['number'],today]
    st.session_state['newcount'] += 1
    count1 = int(st.session_state['newcount'])
    supabase.table("number").update({today:count1}).eq("number",st.session_state['number']).execute()
    numbersql = supabase.table("number").select("*").execute()
    number_df = pd.DataFrame(data = numbersql.data).set_index("number")
    new_counter = int(number_df.loc[st.session_state['number'],today])
    st.session_state['counter'] = new_counter
    st.session_state['remain']  = 10 - st.session_state['counter']
    
def voting():
    if st.session_state['counter'] >= 10:
        st.error(str(st.session_state['number'])+"的使用者你好，今日你已經完成了所有投票，明天可以繼續。") 
        st.session_state['admited'] = 0
    elif st.session_state['counter'] <10:
        st.info(str(st.session_state['number'])+"的使用者你好，今日你已經投了"+ str(st.session_state['counter']) +"次投票，你今天最多可多投"+str(st.session_state['remain'])+"次投票")                 
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Song1 - "+df.loc[st.session_state['r1'],"song_name"])
            st_player(df.loc[st.session_state['r1'],"song"])
            
        with right_column:
            st.header("Song2 - "+df.loc[st.session_state['r2'],"song_name"])
            st_player(df.loc[st.session_state['r2'],"song"])
        st.session_state['song1'] = str("Song1 - "+df.loc[st.session_state['r1'],"song_name"])
        st.session_state['song2'] = str("Song2 - "+df.loc[st.session_state['r2'],"song_name"])
        song = [st.session_state['song1'],st.session_state['song2']]
        st.session_state['votesong'] = st.radio('請投選你認為表現更佳的作品',song,key='vote_radio')    
        st.button("投票",on_click=voted)


def voted():
    st.session_state['repeatvote'] = 1
    rr1 = int(st.session_state['r1'])
    rr2 = int(st.session_state['r2'])
    total2 = int(df.loc[st.session_state['r2'],"total"])
    total2 +=1
    supabase.table("data").update({"total":total2}).eq("id",rr2).execute()
    total1 = int(df.loc[st.session_state['r1'],"total"])
    total1 +=1
    supabase.table("data").update({"total":total1}).eq("id",rr1).execute()
    if st.session_state['vote_radio'] == st.session_state['song1']:
        updatevote1()
        updatecount()
    elif st.session_state['vote_radio'] == st.session_state['song2']:
        updatevote2()
        updatecount()

def refesh():
    st.session_state['repeatvote'] = 0
    st.session_state['r1'] = random.randint(1,10)
    st.session_state['r2'] = random.randint(1,10)
    while st.session_state['r1'] == st.session_state['r2']:
        st.session_state['r1'] = random.randint(1,10)
    
with st.container():
    with st.form(key="checknumber"):
        number = st.text_input("請輸入你的電話號碼")
        num_submitted = st.form_submit_button("提交")
        
if num_submitted:
    st.session_state['number'] = int(number)
    if st.session_state['number'] in number_df.index:
        new_counter = int(number_df.loc[st.session_state['number'],today])
        st.session_state['counter'] = new_counter
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
            st.success('你成功投左'+st.session_state['votesong']+'一票，請按下方更新歌曲button')
            left_column, right_column = st.columns(2)
            with left_column:
                st.write("剛才song1 - "+df.loc[st.session_state['r1'],"song_name"]+"的演唱歌手是"+df.loc[st.session_state['r1'],"name"]+'，以下是他的cover封面設計。')
                img1 = Image.open("website/images/"+df.loc[st.session_state['r1'],"photo"])
                st.image(img1)
            with right_column:
                st.write("剛才song2 - "+df.loc[st.session_state['r2'],"song_name"]+"的演唱歌手是"+df.loc[st.session_state['r2'],"name"]+'，以下是他的cover封面設計。')
                img2 = Image.open("website/images/"+df.loc[st.session_state['r2'],"photo"])
                st.image(img2)
            st.button(label="更新下一組歌曲",on_click=refesh)         
