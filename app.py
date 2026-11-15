import streamlit as st
from modules.core import load_data,enrich
from modules import overview,eda,wellness,clustering,prediction,interventions
st.set_page_config(page_title='ADSSU | Wellness Intelligence',page_icon='📊',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.block-container{padding-top:1.6rem;max-width:1500px}
[data-testid="stMetric"]{background:#17243B;border:1px solid #293C58;border-radius:14px;padding:16px}
h1,h2,h3{letter-spacing:-.025em}
[data-testid="stSidebar"]{border-right:1px solid #2A3B53}
</style>''',unsafe_allow_html=True)
st.sidebar.title('◈ ADSSU')
st.sidebar.caption('OSAS · Wellness Intelligence')
st.sidebar.divider()
upload=st.sidebar.file_uploader('Upload de-identified ADSSU-CWI CSV',type='csv',help='The uploaded data is processed in this application session. Do not deploy a public instance with confidential data.')
if upload is None:
    st.title('ADSSU Comprehensive Wellness Inventory')
    st.info('Upload the authorized de-identified CSV in the sidebar to activate the analytical modules.')
    st.warning('This prototype has no authentication or role-based permissions. Deploy privately with institution-approved controls before using real survey data.')
    st.stop()
try:
    df=load_data(upload.getvalue())
    a=enrich(df)
except Exception as e:
    st.error(f'Unable to read dataset: {e}')
    st.stop()
page=st.sidebar.radio('Research modules',['Executive overview','Exploratory data mining','Objective 1 · Wellness condition','Objective 2 · Behavioral clustering','Objectives 2–3 · Predictors & validation','Objective 4 · Intervention planning'])
st.sidebar.divider()
st.sidebar.caption('Survey-based research only · Not a diagnosis or automated student triage')
if page=='Executive overview':overview.render(df,a)
elif page=='Exploratory data mining':eda.render(df,a)
elif page=='Objective 1 · Wellness condition':wellness.render(df,a)
elif page=='Objective 2 · Behavioral clustering':clustering.render(df,a)
elif page=='Objectives 2–3 · Predictors & validation':prediction.render(df,a)
else:interventions.render(df,a)
