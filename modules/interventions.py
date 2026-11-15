import pandas as pd
import streamlit as st
import plotly.express as px
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = ["#0F766E", "#2563EB", "#D97706", "#7C3AED", "#0891B2"]
from .core import services,protected_table,download_csv
from .theme import polish,TEAL

def render(df,a):
    st.markdown('### Student support program demand')
    st.info('Primary measure: respondents explicitly selecting a service. This is expressed demand, not confirmed eligibility. A respondent may select multiple services.')
    s=services(df)
    if s.empty:st.warning('No service selections found.');return
    n=a.College.value_counts()
    counts=s.groupby(a.College).sum()
    safe=protected_table(counts,n)
    options=['All colleges']+safe.index.tolist()
    selected=st.selectbox('College',options)
    view=safe if selected=='All colleges' else safe.loc[[selected]]
    st.dataframe(view.style.format(na_rep='Suppressed',precision=0),use_container_width=True)
    st.plotly_chart(polish(px.imshow(view,aspect='auto',color_continuous_scale='Teal',title='Requested services by college · small counts hidden'),max(420,70*len(view))),use_container_width=True)
    download_csv(view,'adssu_suppressed_program_demand.csv','Download suppressed program matrix')
    st.subheader('Service request rates by college')
    rates=counts.div(n,axis=0)*100
    rates=rates.loc[safe.index].where(safe.notna())
    st.dataframe(rates.round(1).style.format(na_rep='Suppressed'),use_container_width=True)
    st.subheader('Suggested OSAS program pathways')
    interventions=pd.DataFrame([
      ('Academic coaching','Academic engagement challenges','Study skills, adviser consultations, tutoring'),
      ('Food and financial support','Self-reported food or financial strain','Confidential assessment for scholarships, pantry and transport support'),
      ('Counseling and mental health','Low WHO-5 screening or voluntary request','Offer confidential professional assessment and counseling'),
      ('Peer belonging','Limited social support','Peer mentoring and facilitated student groups'),
      ('Digital wellness','Sleep disruption or digital stress','Digital boundaries and sleep education'),
      ('Housing support','Housing instability response','Safe housing referral and assistance'),
      ('Service awareness','Help-seeking knowledge gaps','OSAS orientation and confidential access information'),
      ('Urgent safety response','Direct safety disclosures','Restricted, prompt human-led triage under approved protocol')],columns=['Program','Exploratory signal','Recommended action'])
    st.dataframe(interventions,hide_index=True,use_container_width=True)
    st.warning('This is an aggregate planning dashboard. It cannot identify or contact individual students. Safety flags must be handled separately in a restricted OSAS workflow.')
