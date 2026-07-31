import pandas as pd
cols = [
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
df = pd.DataFrame([[0]*13], columns=cols)
df.to_csv('test_tavi_real.csv', index=False)
print('建立完成')
