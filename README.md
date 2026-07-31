# CVD Risk Stratification Web Application

A Django-based clinical decision support web application for cardiovascular disease (CVD) risk stratification, developed as part of an Applied Bioinformatics dissertation at King's College London. The application uses machine learning models trained on UK Biobank data to predict individual CVD risk, with support for both individual patient assessments and batch prediction.

---

## Features

- **Patient Portal** — Multi-domain questionnaire covering sociodemographics, lifestyle, health history, family history, sex-specific factors, and psychosocial factors
- **Risk Prediction** — Cox proportional hazards and Random Forest models with MRMR feature selection, producing a probability score and percentile rank against the UK Biobank population
- **Explainability** — SHAP-based feature importance to highlight the top drivers of each patient's risk score
- **Clinician Dashboard** — Clinicians can view and compare individual patient results and assessment history
- **Batch Prediction** — Admin users can upload a CSV of multiple patients and receive predictions for all rows simultaneously
- **Variable Distribution Explorer** — Interactive chart comparing uploaded patient cohort values against UK Biobank reference distributions (decile charts for continuous variables; categorical bar charts for binary/categorical variables)
- **Role-Based Access** — Separate interfaces and permissions for patients, clinicians, and administrators

---

## Models

| Model | Feature Domains | Algorithm |
|---|---|---|
| Model 1 | Sociodemographics | Cox-PH |
| Model 2 | Sociodemographics + Health & Medical History | Cox-PH |
| Model 3 | Sociodemographics + Health + Sex-Specific Factors | Cox-PH |
| Model 7 (Full) | All domains (Sociodemographics, Health, Sex-Specific, Early Life, Family History, Lifestyle, Psychosocial) | Random Forest |
| Full + QRISK + Metabolomics | All domains + QRISK3 features + NMR metabolomics + PRS | Cox-PH |
| SSF | Sex-Specific Factors | Random Forest |
| TAVI | TAVI-specific features | Random Forest |

---

## Tech Stack

- **Backend:** Python 3.11, Django 5.2.3
- **Machine Learning:** scikit-learn 1.6.1, scikit-survival 0.24.1, SHAP
- **Data Processing:** pandas 1.5.3, numpy 1.25.2
- **Database:** MySQL
- **Frontend:** Bootstrap 5, Chart.js 4.4.1, Tom Select 2.3.1
- **Other:** joblib, scipy, survshap

---

## Setup

### Prerequisites

- Python 3.11
- MySQL server

### Installation

```bash
# Clone the repository
git clone https://github.com/andy-gif813/CVD_prediction_website.git
cd CVD_prediction_website

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_sanj.txt
```

### Database

Create a MySQL database and update `config/settings.py` with your credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
    }
}
```

Then run migrations:

```bash
python manage.py migrate
```

The database schema is available in `database/schema.sql`.

### Static Files

```bash
python manage.py collectstatic
```

---

## Running the Application

```bash
python manage.py runserver
```

Navigate to: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

---

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| Patient | joe.marley@gmail.com | Ilovemusic00 |
| Clinician | testclinician@example.com | securepassword123 |

Admin access is available at `/admin/dashboard/` after creating a superuser with `python manage.py createsuperuser`.

---

## Batch Prediction

Admins can upload a CSV of patient feature values at `/batch-prediction/`. The CSV must follow the column format specified in `static/downloads/data_entry_template.csv`. Boolean columns should use `True`/`False` or `1`/`0`.

The Variable Distribution Explorer on the batch results page displays per-variable distributions for the uploaded cohort alongside UK Biobank reference data from `static/data/ukb_distributions.json`.

---

## Project Structure

```
├── accounts/               # Main app: views, models, forms, URLs
│   ├── views.py            # All view logic including prediction pipeline
│   ├── models.py           # Patient, clinician, assessment models
│   └── feature_calculators/  # Per-model feature extraction
├── config/                 # Django project settings and URLs
├── model_files/            # Trained ML models (.pkl), imputers, scalers
├── static/
│   ├── data/               # UK Biobank reference distributions (JSON)
│   └── downloads/          # Feature documentation and data entry template
├── templates/              # HTML templates (Bootstrap 5)
├── Questionnaire_data/     # Questionnaire mapping files
└── database/               # SQL schema files
```

---

## Data Sources

- **UK Biobank** — Primary training dataset (approx. 500,000 participants). Access requires application via [ukbiobank.ac.uk](https://www.ukbiobank.ac.uk).
- **NMR Metabolomics** — Reference distributions from Julkunen et al. (2023), *Nature Communications*, based on 118,461 UK Biobank participants.
- **QRISK3** — Clinical risk features following the QRISK3 algorithm (Hippisley-Cox et al., 2017).
- **Polygenic Risk Scores (PRS)** — Standardised scores (approx. N(0,1)) derived from UK Biobank genetic data.

> Note: Model files (`.pkl`) and raw UK Biobank data are not included in this repository due to data access restrictions.

---

## Contributors

This project was developed collaboratively as a group project at King's College London, Applied Bioinformatics MSc.
