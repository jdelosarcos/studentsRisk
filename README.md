# ADSSU-CWI Wellness Intelligence — Modular Streamlit App

## Run locally

```bash
python -m venv .venv
# Activate .venv (Windows: .venv\Scripts\activate; macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

Upload the authorized **de-identified** ADSSU-CWI CSV from the sidebar. The application intentionally does not bundle any student dataset. Do not commit CSV files to GitHub.

## Modules

- `modules/core.py`: cached loading, schema validation, WHO-5 and PHQ-9 scoring, domain construction, service parsing, disclosure suppression
- `modules/overview.py`: institutional overview
- `modules/eda.py`: exploratory data mining
- `modules/wellness.py`: Objective 1
- `modules/clustering.py`: Objective 2 unsupervised analysis (on-demand)
- `modules/prediction.py`: Objective 2 significance and Objective 3 supervised validation (on-demand)
- `modules/interventions.py`: Objective 4 college-level program demand and intervention pathways

## GitHub / Streamlit hosting

1. Create a **private** GitHub repository and upload the application files, preserving directories.
2. Set `app.py` as the Streamlit entrypoint; install packages from `requirements.txt`.
3. Deploy only behind institution-approved authentication and access controls. Public Streamlit Community Cloud hosting is **not appropriate for confidential student records** without institutional security review.
4. Upload a de-identified dataset at runtime. For a production dashboard, replace file upload with a controlled server-side data pipeline and enforce role-based permissions.

## Performance

`st.cache_data` caches data preparation and expensive model results; only the selected module runs. Clustering and supervised training are triggered by buttons, and are not executed during every page navigation. Large survey data or multi-user workloads should use scheduled offline training and cached approved aggregates.

## Methodology and safeguards

WHO-5 scores are calculated from five 0–5 items ×4; values below 50 are screening indicators, not diagnoses. PHQ-9 symptom bands are descriptive and excluded from the predictors. Models use a stratified 80/20 train/test split and 5-fold stratified cross-validation within training data. Clusters are exploratory behavioral segments. Program demand is measured from explicit service selections, not automatic eligibility. Groups and cells under 10 are hidden in intervention tables; this simple suppression is **not a guarantee against inference through overlapping tables**. Review reverse-coding, survey wording, and construct validity with the research team before publication. No row-level safety flags, direct identifiers, or individualized case files are exported. Immediate-danger disclosures and urgent counselor requests require separate confidential human-led processes. The app does not establish student identity or initiate interventions.

**Deployment caution:** This is a research prototype, not a secure clinical or student case-management platform. Session upload and caching do not replace encryption, retention policies, consent, SSO, audit logging, privacy review, and OSAS governance.

### Accessible theme update (November 2026)
The application now uses a consistent light theme with dark metric values, slate labels,
and a teal accent. This resolves unreadable dark-on-dark KPI cards when hosted
in Streamlit Community Cloud. Upload the updated `.streamlit/config.toml`,
`app.py`, and modules together. In Streamlit Cloud, reboot after committing.
If your personal Streamlit theme overrides the app theme, choose **Light** from
Streamlit Settings → Theme.

## Professional interface update
Navigation labels no longer mention research objective numbers. The application now uses a navy navigation sidebar, light content canvas, high-contrast KPI cards, improved Plotly spacing and titles, horizontal college comparisons, tabs, and consistent chart colors. Computation modules remain separate and heavy analysis runs on demand.

**Privacy:** The application does not implement login or access controls. Deploy only to an institution-approved private environment. Aggregates and interactive filtering may still present disclosure risks; obtain privacy review before operational use.
