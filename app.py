from typing import List, Any

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title="AK/ZAHRAA VIDYALAY ADDALAICHENAI")

# Page top configuration
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 10rem;
                    padding-right: 10rem;
                }
                
                [data-testid="stMetricValue"] {
                    font-size: 80px;
                }
                
                div.css-q8sbsg p{
                    font-size: 24px;
               
        </style>
        """, unsafe_allow_html=True)

with open("style.css") as sorc_styl:
    st.markdown(f"<style>{sorc_styl.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>AK/ZAHRAA VIDYALAY ADD-2023/24</h1>", unsafe_allow_html=True)

grad, sep, teach =  st.columns([2,4,2])

with grad:
    st.markdown("<h4 style='text-align: center;'>GREAD: 08</h4>", unsafe_allow_html=True)
with teach:
    st.markdown("<h4 style='text-align: center;'>Class teacher: <u>N.Farjoon</u></h4>", unsafe_allow_html=True)

st.divider()
# Page top configuration

@st.cache_data
def load_data():
    data = pd.read_excel('sahra.xlsx', index_col='index')
    return data

data = load_data()

numric_colo =  []
for col in data.columns:
 if data[col].dtype!=object:
     numric_colo.append(col)

data['avg'] = data.loc[:, numric_colo].mean(axis=1)
sum_col = data.loc[:, numric_colo].sum(axis = 1)


boy, girl, total =  st.columns(3)

with boy:
    x = data.Gender.value_counts()[0]
    st.metric(label="Boys :boy:", value=x)

with girl:
    x = data.Gender.value_counts()[1]
    st.metric(label="Girls :girl:", value=x)

with total:
    st.metric(label="Total Students :school:", value=data.index.value_counts().sum())

pi, sub_bar = st.columns(2)

with pi:
    pi_gender = px.pie(values=data.Gender.value_counts(), names=['Male', 'Female'], hole=0.5).update_layout(showlegend=False)
    st.plotly_chart(pi_gender)

with sub_bar:
    subject_avg = data.loc[:, numric_colo].mean(axis=0).sort_values(ascending=False)
    bar_subj = px.bar(x=subject_avg.index, y=subject_avg.values, title="Comparing Subject Average Scores").update_layout(yaxis_title=None, xaxis_title=None)
    st.plotly_chart(bar_subj)

st.divider()

boy_std, gir_sddt = st.columns(2)

with boy_std:
    boyTic = st.checkbox(label="Boys :boy:", value=1)

with gir_sddt:
    girlTic = st.checkbox(label="Girls :girl:", value=1)

if boyTic and girlTic:
    df = data

elif girlTic:
    df = data[data['Gender'] == "Female"]

elif boyTic:
    df = data[data['Gender']=="Male"]

else:
    df = data

df = df.sort_values(by='avg', ascending=True)

std_bar = px.bar(y=df['name'], x=df["avg"], title="Student Performance", width=1210, height=700).update_layout(yaxis_title=None, xaxis_title=None)
st.plotly_chart(std_bar)

fir_rank, las_rank = st.columns(2)

with fir_rank:
    firstRank = df[df['avg'] == df.avg.max()].index[0]
    st.subheader("Firs Rank")

    name = df._get_value(firstRank, col='name')
    total = sum_col._get_value(firstRank)
    avg = df._get_value(firstRank, col='avg')

    st.success(f"Index: {firstRank} ")
    st.success(f"Name: {name}")
    st.success(f"Total: {total}")
    st.success(f"Average:{avg}")

with las_rank:
    lastRank = df[df['avg'] == df.avg.min()].index[0]
    st.subheader("Last Rank")

    name = df._get_value(lastRank, col='name')
    total = sum_col._get_value(lastRank)
    avg = df._get_value(lastRank, col='avg')

    st.warning(f"Index: {lastRank}")
    st.warning(f"Name: {name}")
    st.warning(f"Total: {total}")
    st.warning(f"Average:{avg}")

st.divider()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

footer="""
<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0E1117;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://nextechgen.github.io/" target="_blank">Zainudeen Rusaid Ahamed</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

