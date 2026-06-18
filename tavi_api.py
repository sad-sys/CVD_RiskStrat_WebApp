from fastapi import FastAPI, UploadFile, File
import joblib
import pandas as pd
import io

app = FastAPI()

model = joblib.load("model_files/batch_models/TAVIModel.pkl")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    FEATURE_COLS = [
    'Age',
    'Diabetes mellitus',
    'Previous smoking history',
    'Hypertension',
    'Creatinine',
    'Atrial fibrillation / Preprocedural heart rhythm',
    'Haemoglobin',
    'Poor mobility',
    'FEV1/FVC ratio',
    'Predicted VC (Predicted Vital Capacity)',
    'Katz Index of Independence',
    'Moderate or greater Tricuspid Regurgitation (TR)',
    'FEV1'
    ]
    df_input = df[FEATURE_COLS] if all(c in df.columns for c in FEATURE_COLS) else df.iloc[:, :13]
    predictions = model.predict_proba(df_input)[:, 1] if hasattr(model, 'predict_proba') else model.predict(df_input)
    
    df['Predicted Risk Score'] = predictions
    
    def risk_category(score):
        if score < 0.5:
            return 'Low Risk'
        else:
            return 'High Risk'
    
    df['Risk Category'] = df['Predicted Risk Score'].apply(risk_category)
    
    return df.to_dict(orient='records')