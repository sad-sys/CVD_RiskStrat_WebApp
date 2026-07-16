import pickle
import numpy as np
import pandas as pd
from feature_calculators.core import calculate_model_features


def run_tree(x, tree):
    node = 0

    while tree["left"][node] != -1:
        feature_idx = tree["feature"][node]
        threshold = tree["threshold"][node]

        if x[feature_idx] <= threshold:
            node = tree["left"][node]
        else:
            node = tree["right"][node]

    return tree["value"][node]


def run_forest(x, forest):
    return np.mean([
        run_tree(x, tree)
        for tree in forest
    ])


def custom_impute(x, imputer, exported_triplets):
    x = np.asarray(x, dtype=float).reshape(1, -1)

    # Record which values were genuinely missing in the raw input
    missing_mask = np.isnan(x)

    # Reproduce IterativeImputer's initial filling step
    x_filled = imputer.initial_imputer_.transform(x)

    # Work with one row
    x_filled = np.asarray(x_filled[0], dtype=float)

    # Apply each fitted estimator in sklearn's stored order
    for triplet in exported_triplets:
        target_idx = triplet["feat_idx"]

        # Only update values that were missing in the original input
        if missing_mask[0, target_idx]:
            neighbor_indices = triplet["neighbor_feat_idx"]
            neighbor_values = x_filled[neighbor_indices]

            prediction = run_forest(
                neighbor_values,
                triplet["forest"],
            )

            # Match IterativeImputer clipping behaviour
            min_value = np.asarray(imputer._min_value)
            max_value = np.asarray(imputer._max_value)

            prediction = np.clip(
                prediction,
                min_value[target_idx],
                max_value[target_idx],
            )

            x_filled[target_idx] = prediction

    return x_filled




def calculate_features(patient_id, submission_id):
    # Step 1: Run core logic to get raw features
    raw_features = calculate_model_features(
        patient_id=patient_id,
        submission_id=submission_id,
        model_name='MRMR_COX_Sociodemographics_Health_and_medical_history_Sex-specific_factors',
        template_path='model_files/feature_templates/model3_SSF_features.xlsx'
    )

    # Step 2: Convert to DataFrame
    df = pd.DataFrame([raw_features])

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
    with open('model_files/imputers/SSFnoDrop_rf.pkl', 'rb') as f:
        imputer = pickle.load(f)

    expected_imputer_features = imputer.feature_names_in_
    df = df.reindex(columns=expected_imputer_features)

    # Step 4: Apply imputer
    #df_imputed = pd.DataFrame(imputer.transform(df), columns=expected_imputer_features)
    exported_triplets = []

    for triplet in imputer.imputation_sequence_:
        rf = triplet.estimator
        exported_forest = []

        for tree in rf.estimators_:
            exported_forest.append({
                "feature": tree.tree_.feature.copy(),
                "threshold": tree.tree_.threshold.copy(),
                "left": tree.tree_.children_left.copy(),
                "right": tree.tree_.children_right.copy(),
                "value": tree.tree_.value[:, 0, 0].copy(),
            })

        exported_triplets.append({
            "feat_idx": int(triplet.feat_idx),
            "neighbor_feat_idx": triplet.neighbor_feat_idx.copy(),
            "forest": exported_forest,
        })

    imputed_array = custom_impute(
        df.iloc[0].to_numpy(dtype=float),
        imputer,
        exported_triplets,
    )

    df_imputed = pd.DataFrame(
        [imputed_array],
        columns=expected_imputer_features,
    )

    # Step 5: Load scaler and align input (if applicable)
    try:
        with open('model_files/scalers/SSFnoDropscaler.pkl', 'rb') as f:
            scaler = pickle.load(f)

        if hasattr(scaler, 'feature_names_in_'):
            df_imputed = df_imputed.reindex(columns=scaler.feature_names_in_, fill_value=0)

        df_scaled = pd.DataFrame(scaler.transform(df_imputed), columns=df_imputed.columns)
    except FileNotFoundError:
        df_scaled = df_imputed

    # Step 6: Save final input to file (optional)
    out_path = f"model_outputs/patient_{patient_id}_model3_input_scaled.csv"
    df_scaled.to_csv(out_path, index=False)

    return df_scaled

    

