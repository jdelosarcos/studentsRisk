import streamlit as st
import plotly.express as px
from .theme import polish,TEAL,BLUE

def render(df,a):
    valid=a.dropna(subset=['WHO5_score'])
    summary=valid.groupby('College').agg(Responses=('WHO5_score','size'),Mean_WHO5=('WHO5_score','mean'),Low_WHO5=('low_wellbeing','sum'))
    summary=summary[summary.Responses>=10].copy()
    summary['Below_50_percent']=100*summary.Low_WHO5/summary.Responses
    summary['Low_WHO5']=summary.Low_WHO5.where(summary.Low_WHO5>=10)
    t1,t2=st.tabs(['College comparisons','Statistical summary'])
    with t1:
        chart=summary.reset_index().sort_values('Mean_WHO5')
        c1,c2=st.columns(2)
        with c1:st.plotly_chart(polish(px.bar(chart,x='Mean_WHO5',y='College',orientation='h',title='Average WHO-5 score by college',color_discrete_sequence=[TEAL])),use_container_width=True)
        with c2:st.plotly_chart(polish(px.bar(chart,x='Below_50_percent',y='College',orientation='h',title='Share of respondents below WHO-5 threshold',labels={'Below_50_percent':'Percentage (%)'},color_discrete_sequence=[BLUE])),use_container_width=True)
    with t2:
        st.dataframe(valid[['WHO5_score','PHQ9_score']].describe().round(2),use_container_width=True)
        st.dataframe(summary.round(2),use_container_width=True)
    st.caption('Screening results are not diagnoses. College groups with fewer than 10 responses are excluded; small counts are suppressed in tables.')
