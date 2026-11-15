import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score,adjusted_rand_score
from .core import domains,protected_table

@st.cache_data(show_spinner='Computing behavioral clusters...',max_entries=3)
def fit_clusters(d):
    eligible=d.notna().sum(axis=1)>=5
    z=StandardScaler().fit_transform(SimpleImputer(strategy='median').fit_transform(d.loc[eligible]))
    candidates=[]
    for k in range(2,min(7,len(z))):
        km=KMeans(n_clusters=k,n_init=20,random_state=42).fit(z)
        candidates.append({'k':k,'silhouette':silhouette_score(z,km.labels_,sample_size=min(1000,len(z)),random_state=42),'min_cluster':int(np.bincount(km.labels_).min())})
    q=pd.DataFrame(candidates)
    good=q[q.min_cluster>=max(10,int(.03*len(z)))]
    k=int((good if not good.empty else q).sort_values('silhouette',ascending=False).iloc[0].k)
    km=KMeans(n_clusters=k,n_init=20,random_state=42).fit(z)
    pc=PCA(n_components=2).fit_transform(z)
    labels=pd.Series(km.labels_+1,index=d.loc[eligible].index,name='Cluster')
    scatter=pd.DataFrame({'PC1':pc[:,0],'PC2':pc[:,1],'Cluster':labels.astype(str).values},index=labels.index)
    profile=d.loc[eligible].groupby(labels).mean()
    ari=np.mean([adjusted_rand_score(km.labels_,KMeans(n_clusters=k,n_init=20,random_state=s).fit_predict(z)) for s in [7,19,123,2026]])
    return q,labels,scatter,profile,ari

def render(df,a):
    st.header('Behavioral clustering')
    st.caption('Unsupervised clustering uses behavioral domains, excluding wellness outcome, safety responses, college, and direct identifiers.')
    if not st.button('Run clustering',type='primary',key='run_clusters') and 'cluster_ready' not in st.session_state:return
    st.session_state.cluster_ready=True
    d=domains(df,reverse=True)
    q,labels,scatter,profile,ari=fit_clusters(d)
    st.metric('Cluster stability · mean adjusted Rand index',f'{ari:.3f}')
    st.plotly_chart(px.line(q,x='k',y='silhouette',markers=True,title='Cluster selection'),use_container_width=True)
    st.plotly_chart(px.scatter(scatter,x='PC1',y='PC2',color='Cluster',opacity=.65,title='PCA behavioral map'),use_container_width=True)
    st.plotly_chart(px.imshow(profile,text_auto='.2f',aspect='auto',title='Mean domain scores by cluster'),use_container_width=True)
    cross=pd.crosstab(a.loc[labels.index,'College'],labels)
    safe=protected_table(cross,a.College.value_counts())
    st.subheader('College × cluster (small cells suppressed)')
    st.dataframe(safe,use_container_width=True)
    st.caption('Cluster labels are descriptive, not validated risk tiers. Reverse-coding requires expert item-level verification.')
