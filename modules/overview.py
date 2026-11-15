import streamlit as st
import plotly.express as px
from .core import protected_table

def render(df,a):
    st.header('Executive overview')
    valid=a.WHO5_score.notna()
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Survey responses',f'{len(df):,}')
    c2.metric('Colleges',a.College.nunique())
    c3.metric('Valid WHO-5',f'{valid.sum():,}')
    c4.metric('WHO-5 below 50',f'{100*a.loc[valid,"low_wellbeing"].mean():.1f}%' if valid.any() else 'N/A')
    counts=a.College.value_counts().rename_axis('College').reset_index(name='Responses')
    counts=counts[counts.Responses>=10]
    st.plotly_chart(px.bar(counts,x='College',y='Responses',title='Survey participation by college'),use_container_width=True)
    st.info('This dashboard reports survey responses, not verified unique students or clinical diagnoses. Screening findings require human interpretation.')
