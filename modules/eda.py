import streamlit as st
import pandas as pd
import plotly.express as px
from .core import domains,services

def render(df,a):
    st.header('Exploratory data mining')
    quality=pd.DataFrame({'Variable':df.columns,'Missing':df.isna().sum().values,'Missing %':(df.isna().mean()*100).values,'Distinct':df.nunique(dropna=True).values})
    st.dataframe(quality.sort_values('Missing %',ascending=False).head(30),hide_index=True,use_container_width=True)
    st.plotly_chart(px.histogram(a,x='WHO5_score',nbins=25,title='WHO-5 score distribution'),use_container_width=True)
    st.plotly_chart(px.histogram(a,x='PHQ9_band',title='PHQ-9 symptom bands (descriptive only)'),use_container_width=True)
    d=domains(df)
    st.plotly_chart(px.imshow(d.corr(method='spearman'),text_auto='.2f',aspect='auto',title='Spearman correlations between survey domains'),use_container_width=True)
    s=services(df)
    if not s.empty:
        overall=s.sum().sort_values(ascending=False).rename_axis('Program').reset_index(name='Requests')
        st.plotly_chart(px.bar(overall,x='Requests',y='Program',orientation='h',title='Self-reported requested programs'),use_container_width=True)
        st.caption('These are overlapping program selections. Survey items may not form validated psychometric scales.')
