import pandas as pd
import streamlit as st
import plotly.express as px
from .core import domains,services
from .theme import polish,TEAL,BLUE

def render(df,a):
    quality=pd.DataFrame({'Variable':df.columns,'Missing':df.isna().sum().values,'Missing %':(df.isna().mean()*100).values,'Distinct':df.nunique(dropna=True).values})
    t1,t2,t3=st.tabs(['Data quality','Survey distributions','Behavioral relationships'])
    with t1:
        c1,c2,c3=st.columns(3)
        c1.metric('Survey variables',len(df.columns));c2.metric('Missing values',f'{int(df.isna().sum().sum()):,}');c3.metric('Complete rows',f'{int(df.notna().all(axis=1).sum()):,}')
        top=quality.nlargest(15,'Missing %').sort_values('Missing %')
        st.plotly_chart(polish(px.bar(top,x='Missing %',y='Variable',orientation='h',title='Fields with the most missing responses',color_discrete_sequence=[BLUE]),540),use_container_width=True)
        with st.expander('Full data quality table'):
            st.dataframe(quality.sort_values('Missing %',ascending=False),hide_index=True,use_container_width=True)
    with t2:
        c1,c2=st.columns(2)
        with c1:st.plotly_chart(polish(px.histogram(a,x='WHO5_score',nbins=22,title='WHO-5 distribution',color_discrete_sequence=[TEAL])),use_container_width=True)
        with c2:
            bands=a.PHQ9_band.value_counts().rename_axis('Band').reset_index(name='Responses')
            st.plotly_chart(polish(px.bar(bands,x='Band',y='Responses',title='PHQ-9 symptom categories',color_discrete_sequence=[BLUE])),use_container_width=True)
        s=services(df)
        if not s.empty:
            counts=s.sum().sort_values(ascending=False).head(15).sort_values().rename_axis('Program').reset_index(name='Requests')
            st.plotly_chart(polish(px.bar(counts,x='Requests',y='Program',orientation='h',title='Most requested student services',color_discrete_sequence=[TEAL]),540),use_container_width=True)
            st.caption('Program requests overlap; do not sum as unique students.')
    with t3:
        d=domains(df)
        corr=d.corr(method='spearman')
        fig=px.imshow(corr,text_auto='.2f',color_continuous_scale='RdBu_r',zmin=-1,zmax=1,title='Spearman associations among survey domains',aspect='auto')
        st.plotly_chart(polish(fig,560),use_container_width=True)
        st.caption('Exploratory domain scores are not validated psychometric scales. Correlations are not causal.')
