import pickle
import numpy as np
import pandas as pd
from feature_calculators.core import calculate_model_features
print("New Version 20/02")


def calculate_features(patient_id, submission_id):
    # Step 1: Run core logic to get raw features
    raw_features = calculate_model_features(
        patient_id=patient_id,
        submission_id=submission_id,
        model_name='MRMR_COX_Sociodemographics',
        template_path='model_files/feature_templates/model1_sociodemographic_features.xlsx'
    )

    # Step 2: Convert to DataFrame
    df = pd.DataFrame([raw_features])
    print("The Raw_Features are ",df)
    # Fix misnamed features
    if 'clinicalrisk_Age.at.recruitment' in df.columns:
        df.rename(columns={'clinicalrisk_Age.at.recruitment': 'Age.at.recruitment'}, inplace=True)

    prefix = df.columns[0].split("...")[0]
    print("The first prefix is", prefix)

    for col in df.columns:
        newPrefix = col.split("...")[0]
        print("Current prefix is", newPrefix)

        if newPrefix != prefix:
            prefix = newPrefix
            dfWithPrefix = df[[c for c in df.columns if c.startswith(prefix)]]

            print("Columns with that prefix", dfWithPrefix.columns)

            # If any value exists in this prefix group, fill NaNs in this group only
            if dfWithPrefix.notna().any().any():
                df.loc[:, dfWithPrefix.columns] = dfWithPrefix.fillna(0)

            for c in dfWithPrefix.columns:
                non_na = dfWithPrefix[c].dropna()

                if not non_na.empty:
                    print(f"Column: {c}")
                    print(non_na.values)

            print("All columns, df With Prefix", dfWithPrefix.columns)

    # Step 3: Load imputer and align input
    with open('model_files/imputers/model1_sociodemographics_rf (1).pkl', 'rb') as f:
        imputer = pickle.load(f)

    expected_features = imputer.feature_names_in_
    print("RAW FEATURES KEYS:")
    print(df.columns.tolist())
    print("AGE VALUE BEFORE REINDEX:")
    print(df.get("clinicalrisk_Age.at.recruitment"))
    print("IMPUTER EXPECTS:")
    print(expected_features[-5:])  # just show last few
    if 'clinicalrisk_Age.at.recruitment' in df.columns:
        df.rename(columns={'clinicalrisk_Age.at.recruitment': 'Age.at.recruitment'}, inplace=True)
    df = df.reindex(columns=expected_features)

    
    # Step 4: Apply imputer
    print(type(imputer))
    print(hasattr(imputer, "n_iter_"))
    print("COUNT ZEROS:", (df == 0).sum().sum())
    print("COUNT NaNs:", df.isna().sum().sum())      
    df_imputed = pd.DataFrame(imputer.transform(df), columns=expected_features)
    
    

    # Step 5: Load and apply scaler (if applicable)
    try:
        with open('model_files/scalers/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        if hasattr(scaler, 'feature_names_in_'):
            df_imputed = df_imputed.reindex(columns=scaler.feature_names_in_)

        df_scaled = pd.DataFrame(scaler.transform(df_imputed.values), columns=df_imputed.columns)
    except FileNotFoundError:
        print("Scaler,",scaler,", NOT found")
        df_scaled = df_imputed  # Use imputed if no scaler is defined

    # After imputation + optional scaling
    if 'Age.at.recruitment' in df_scaled.columns:
        df_scaled.rename(columns={'Age.at.recruitment': 'clinicalrisk_Age.at.recruitment'}, inplace=True)


    # Step 6: Save final input to file (optional)
    out_path = f"model_outputs/patient_{patient_id}_model1_input_scaled.csv"
    df_scaled.to_csv(out_path, index=False)

    return df_scaled

