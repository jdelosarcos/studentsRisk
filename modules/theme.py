import streamlit as st
import plotly.express as px

NAVY='#14263F'; TEAL='#087F78'; BLUE='#3272B8'; MUTED='#64748B'; PALETTE=[TEAL,BLUE,'#E0A44B','#7B69B4','#3998A4','#DB796F']

def setup():
    px.defaults.template='plotly_white'
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown('''<style>
    .stApp {background:#F7F9FC;color:#172B45}
    .block-container {max-width:1480px;padding-top:2rem;padding-bottom:4rem}
    [data-testid="stSidebar"] {background:#14263F!important;border-right:0}
    [data-testid="stSidebar"] * {color:#EAF2F9!important}
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {background:#233A55;border-radius:12px;padding:10px}
    [data-testid="stSidebar"] [role="radiogroup"] label {padding:9px 10px;border-radius:9px;margin:3px 0}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#29425F}
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:#235B67!important}
    h1,h2,h3 {color:#14263F!important;letter-spacing:-.035em}
    h1 {font-size:2rem!important} h2 {font-size:1.4rem!important}
    [data-testid="stMetric"] {background:#FFFFFF!important;border:1px solid #E3EAF2;border-radius:16px;padding:20px;box-shadow:0 4px 18px #14263F0A}
    [data-testid="stMetricLabel"] *,[data-testid="stMetricLabel"] {color:#53677F!important;font-weight:600!important;opacity:1!important}
    [data-testid="stMetricValue"] *,[data-testid="stMetricValue"] {color:#14263F!important;font-size:2rem!important;font-weight:750!important;opacity:1!important}
    [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {background:#FFFFFF;border:1px solid #E3EAF2;border-radius:16px;padding:9px;box-shadow:0 3px 14px #14263F08}
    [data-testid="stTabs"] button {font-weight:650}
    .hero {padding:24px 28px;border-radius:18px;background:linear-gradient(105deg,#14263F,#21586A);color:#fff;margin:0 0 20px}
    .hero .eyebrow {font-size:12px;font-weight:700;letter-spacing:.15em;color:#A8E1DC;margin-bottom:7px}
    .hero .heading {font-size:27px;font-weight:750;line-height:1.2;color:white}
    .hero .sub {color:#D4E5EE;font-size:14px;margin-top:8px}
    .stButton>button[kind="primary"] {background:#087F78;border-color:#087F78;border-radius:9px}
    @media(max-width:700px){.hero .heading{font-size:21px}.block-container{padding:1rem}}
    </style>''',unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><div class="eyebrow">ADSSU · OSAS WELLNESS INTELLIGENCE</div><div class="heading">{title}</div><div class="sub">{subtitle}</div></div>',unsafe_allow_html=True)

def polish(fig,height=420):
    fig.update_layout(template='plotly_white',height=height,margin=dict(l=18,r=22,t=55,b=30),paper_bgcolor='#FFFFFF',plot_bgcolor='#FFFFFF',font=dict(family='Arial',color=NAVY,size=12),title_font=dict(size=17,color=NAVY),legend_title_text='',hoverlabel=dict(bgcolor='white',font_color=NAVY))
    fig.update_xaxes(showgrid=True,gridcolor='#EDF2F7',zeroline=False)
    fig.update_yaxes(showgrid=False,zeroline=False)
    return fig
