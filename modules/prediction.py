import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = ["#0F766E", "#2563EB", "#D97706", "#7C3AED", "#0891B2"]
from scipy.stats import mannwhitneyu,chi2_contingency
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import train_test_split,StratifiedKFold,cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score,average_precision_score,balanced_accuracy_score,f1_score,recall_score,confusion_matrix,brier_score_loss,roc_curve
from sklearn.inspection import permutation_importance
from .core import domains
from .theme import polish

def features(df):
    x=domains(df)
    for key,col in {'age':'Age','college':'College','year_level':'Year level/status','internet_access':df.columns[14],'housing_status':df.columns[43],'food_last':df.columns[44],'food_balanced':df.columns[45],'food_cut_meal':df.columns[46],'food_hungry':df.columns[49]}.items():
        x[key]=pd.to_numeric(df[col],errors='coerce') if key=='age' else df[col].astype('object')
    return x

@st.cache_data(show_spinner='Running significance tests...',max_entries=3)
def significance(x,y):
    rows=[]
    for col in x:
        s=x[col]
        if pd.api.types.is_numeric_dtype(s):
            aa=s[y==1].dropna();bb=s[y==0].dropna()
            if min(len(aa),len(bb))<5:continue
            stat,p=mannwhitneyu(aa,bb); effect=float(aa.median()-bb.median());method='Mann–Whitney U'
        else:
            tab=pd.crosstab(s.fillna('Missing'),y)
            if min(tab.shape)<2:continue
            stat,p,_,_=chi2_contingency(tab)
            effect=float(np.sqrt(stat/(tab.values.sum()*max(1,min(tab.shape)-1))));method='Chi-square'
        rows.append({'Feature':col,'Test':method,'Statistic':stat,'p_value':p,'Effect':effect})
    r=pd.DataFrame(rows)
    if len(r):r['FDR_q']=multipletests(r.p_value,method='fdr_bh')[1]
    return r.sort_values('FDR_q')

@st.cache_data(show_spinner='Training models and running cross-validation...',max_entries=2)
def train(x,y):
    numeric=x.select_dtypes(include='number').columns.tolist();categorical=[c for c in x if c not in numeric]
    prep=ColumnTransformer([('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),numeric),('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('encode',OneHotEncoder(handle_unknown='ignore'))]),categorical)])
    models={'Logistic regression':LogisticRegression(max_iter=2000,class_weight='balanced',random_state=42),'Random forest':RandomForestClassifier(n_estimators=200,min_samples_leaf=5,class_weight='balanced',random_state=42,n_jobs=-1)}
    xt,xv,yt,yv=train_test_split(x,y,test_size=.2,stratify=y,random_state=42)
    cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
    rows=[]
    for name,model in models.items():
        pipe=Pipeline([('preprocess',prep),('model',model)])
        scores=cross_validate(pipe,xt,yt,cv=cv,scoring={'roc_auc':'roc_auc','f1':'f1','recall':'recall','balanced_accuracy':'balanced_accuracy','average_precision':'average_precision'},n_jobs=1)
        row={'Model':name}
        for metric in ['roc_auc','f1','recall','balanced_accuracy','average_precision']:
            row[metric+'_mean']=scores['test_'+metric].mean();row[metric+'_sd']=scores['test_'+metric].std(ddof=1)
        rows.append(row)
    comparison=pd.DataFrame(rows).sort_values('roc_auc_mean',ascending=False)
    selected=comparison.iloc[0].Model
    best=Pipeline([('preprocess',prep),('model',models[selected])]).fit(xt,yt)
    prob=best.predict_proba(xv)[:,1];pred=(prob>=.5).astype(int)
    metrics={'ROC-AUC':roc_auc_score(yv,prob),'Average precision':average_precision_score(yv,prob),'Balanced accuracy':balanced_accuracy_score(yv,pred),'Recall':recall_score(yv,pred),'F1':f1_score(yv,pred),'Brier score':brier_score_loss(yv,prob)}
    imp=permutation_importance(best,xv,yv,scoring='roc_auc',n_repeats=5,random_state=42,n_jobs=1)
    importance=pd.DataFrame({'Feature':x.columns,'Mean AUC drop':imp.importances_mean}).sort_values('Mean AUC drop',ascending=False)
    fpr,tpr,_=roc_curve(yv,prob)
    return comparison,selected,metrics,importance,pd.DataFrame({'FPR':fpr,'TPR':tpr}),confusion_matrix(yv,pred)

def render(df,a):
    st.markdown('### Predictive modeling and evidence')
    valid=a.low_wellbeing.notna()
    x=features(df).loc[valid];y=a.loc[valid,'low_wellbeing'].astype(int)
    st.subheader('Exploratory statistical significance')
    if st.button('Run significance tests',key='sig') or st.session_state.get('sig_ready'):
        st.session_state.sig_ready=True
        result=significance(x,y)
        st.dataframe(result.round(4),hide_index=True,use_container_width=True)
    st.subheader('Classification and 5-fold cross-validation')
    if st.button('Train and evaluate models',type='primary',key='train') or st.session_state.get('train_ready'):
        st.session_state.train_ready=True
        comp,name,metrics,imp,roc,cm=train(x,y)
        st.success(f'Selected by training CV ROC-AUC: {name}')
        st.dataframe(comp.round(3),hide_index=True,use_container_width=True)
        st.dataframe(pd.DataFrame([metrics]).round(3),hide_index=True,use_container_width=True)
        st.plotly_chart(polish(px.line(roc,x='FPR',y='TPR',title='Held-out ROC curve')),use_container_width=True)
        st.plotly_chart(polish(px.imshow(cm,text_auto=True,color_continuous_scale='Teal',labels={'x':'Predicted','y':'Observed'},title='Held-out confusion matrix')),use_container_width=True)
        st.plotly_chart(polish(px.bar(imp.head(12).sort_values('Mean AUC drop'),x='Mean AUC drop',y='Feature',orientation='h',title='Predictor importance on held-out data'),520),use_container_width=True)
    st.warning('Prediction is of WHO-5 screening status, not a diagnosis. Threshold 0.5 is not a validated clinical action cutoff; never automate individual referrals.')
