import pandas as pd
import streamlit as st
import plotly.express as px
from .theme import polish,TEAL,BLUE

def render(df,a):
    valid=a.WHO5_score.notna()
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Survey responses',f'{len(df):,}')
    c2.metric('College categories',f'{a.College.nunique():,}')
    c3.metric('Valid WHO-5 screenings',f'{valid.sum():,}')
    c4.metric('WHO-5 below 50',f'{100*a.loc[valid,"low_wellbeing"].mean():.1f}%' if valid.any() else 'N/A')
    st.markdown('### Participation & screening overview')
    counts=a.College.value_counts().rename_axis('College').reset_index(name='Responses')
    counts=counts[counts.Responses>=10].sort_values('Responses')
    c1,c2=st.columns([1.2,1])
    with c1:
        fig=px.bar(counts,x='Responses',y='College',orientation='h',text='Responses',title='Survey participation by college',color_discrete_sequence=[TEAL])
        fig.update_traces(textposition='outside',cliponaxis=False)
        st.plotly_chart(polish(fig,430),use_container_width=True)
    with c2:
        who=a.loc[valid,'WHO5_score']
        fig=px.histogram(x=who,nbins=22,title='Well-being score distribution',labels={'x':'WHO-5 score','y':'Responses'},color_discrete_sequence=[BLUE])
        fig.add_vline(x=50,line_dash='dash',line_color='#D97757',annotation_text='Screening threshold')
        st.plotly_chart(polish(fig,430),use_container_width=True)
    st.caption('Respondent counts are not verified unique-student counts. WHO-5 below 50 is a screening indicator, not a diagnosis.')
