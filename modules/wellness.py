import streamlit as st
import plotly.express as px
from .core import protected_table

def render(df,a):
    st.header('Objective 1 · Wellness condition')
    valid=a.dropna(subset=['WHO5_score'])
    st.dataframe(valid[['WHO5_score','PHQ9_score']].describe().round(2),use_container_width=True)
    summary=valid.groupby('College').agg(Responses=('WHO5_score','size'),Mean_WHO5=('WHO5_score','mean'),Low_WHO5=('low_wellbeing','sum'))
    summary=summary[summary.Responses>=10].copy()
    summary['Low_WHO5_percent']=100*summary.Low_WHO5/summary.Responses
    summary['Low_WHO5']=summary.Low_WHO5.where(summary.Low_WHO5>=10)
    st.dataframe(summary.round(2),use_container_width=True)
    st.plotly_chart(px.bar(summary.reset_index(),x='College',y='Mean_WHO5',title='Mean WHO-5 by college'),use_container_width=True)
    st.caption('WHO-5 below 50 indicates a screening signal; PHQ-9 categories are symptom descriptions, not diagnoses. Counts under 10 are suppressed.')
