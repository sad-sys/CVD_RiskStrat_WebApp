import pandas as pd
import numpy as np
import os
import re
from django.db import connections
from django.utils import timezone
from accounts.models import (
    CVD_risk_Responses,
    CVD_ModelFeatureMappings,
    CVD_Risk_FeatureThresholds,
    CVD_Risk_CalculatedFeatures,
    FeatureOptionMapping,
    ML_Models,
)

def calculate_model_features(patient_id, submission_id, model_name, template_path):
    """
    Reusable feature calculation logic for any model.
    Ensures conditional/unanswered features (e.g. sex-specific) are defaulted to 0.
    """
    connections.close_all()  # Ensure no leftover transactions
    
    # 1. Load expected features from Excel
    try:
        feature_order = pd.read_excel(template_path, header=None)[0].tolist()
    except Exception as e:
        print(f"❌ Error loading feature template: {e}")
        return

    # 2. Load model from DB
    try:
        model = ML_Models.objects.get(model_name=model_name)
    except ML_Models.DoesNotExist:
        print(f"❌ Model not found in DB: {model_name}")
        return

    # 3. Load feature mappings
    mappings = CVD_ModelFeatureMappings.objects.filter(model=model).select_related('input_feature')
    model_features = {m.input_feature.feature_name: m.input_feature for m in mappings}
    print("DOES MODEL CONTAIN Number.in.household tertiles?")
    for k in model_features.keys():
        if "Number.in.household" in k:
            print(k)
    
    # 4. Initialize feature values to 0
    #feature_values = {fname: 0 for fname in feature_order}
    feature_values = {fname: np.nan for fname in feature_order}

    # 5. Tertile grouping
    tertile_groups = {}
    for fname in feature_order:
        #Sadiq change
        clean_name = re.sub(r'^category_.*?_ts_', '', fname).strip()
        #clean_name = fname
        if any(suffix in clean_name for suffix in ['_Lower.third', '_Middle.third', '_Upper.third']):
            base = clean_name.rsplit('_', 1)[0]
            tertile_groups.setdefault(base, []).append((fname, clean_name))

    # 6. Calculate feature values from responses
    for fname in feature_order:
        #Sadiq Change
        #full_feature_name = re.sub(r'^category_.*?_ts_', '', fname).strip()
        full_feature_name = fname
        #Sadiq change 2
        #if full_feature_name == "Age.at.recruitment":
        #    full_feature_name = "clinicalrisk_Age.at.recruitment"

        if full_feature_name not in model_features:
            print(f"⚠️ Input feature not in DB: {full_feature_name}")
            continue

        feature_obj = model_features[full_feature_name]
        question = feature_obj.question
        try:
            # ALWAYS reset
            response = (
                CVD_risk_Responses.objects
                .filter(
                    patient_id=patient_id,
                    submission_id=submission_id,
                    question=question
                )
                .order_by("-response_id")
                .first()
)

            # Optional debug
            if "Number.in.household" in full_feature_name:
                print("🔎 FEATURE:", full_feature_name)
                print("🔎 QUESTION TEXT:", question.question_text)
                print("🔎 RESPONSE FOUND:", response)

            if not response:
                continue

            print("RESPONSE TYPE:", response.response_type)
            print("NUMERIC VALUE:", response.numeric_response)
            if "Number.in.household" in full_feature_name:
                print("🔎 RESPONSE FOUND:", response)

            # If no response exists, default 0 already set — skip
            if not response:
                continue
            print("RESPONSE TYPE:", response.response_type)
            print("NUMERIC VALUE:", response.numeric_response)
            # === A. Numeric (Tertile) ===
            if response.response_type == 'Enter integer answer' and response.numeric_response is not None:
                val = response.numeric_response
                #Sadiq change
                base_name = full_feature_name.rsplit('_', 1)[0]
                #clean_base_name = re.sub(r'^category_.*?_ts_', '', full_feature_name).strip()
                #clean_base_name = clean_base_name.rsplit('_', 1)[0]
                #base_name = re.sub(r'^category_.*?_ts_', '', full_feature_name).strip()
                #base_name = base_name.rsplit('_', 1)[0]
                clean_base_name = re.sub(r'^category_.*?_ts_', '', full_feature_name).strip()
                clean_name = re.sub(r'^category_.*?_ts_', '', full_feature_name).strip()
                if clean_name.startswith("clinicalrisk_"):
                    base_clean = clean_name.replace("clinicalrisk_", "")
                else:
                    base_clean = clean_name.split("_")[0]
                
                print("FULL FEATURE:", full_feature_name)
                print("CLEAN NAME:", clean_name)
                print("BASE CLEAN:", base_clean)

                #print("Tertile groups is",tertile_groups)
                print("BASE_CLEAN:", repr(base_clean))
                print("TERTILE KEYS:", [repr(k) for k in tertile_groups.keys()])
                if base_clean in tertile_groups:
                    triplet = tertile_groups[base_clean]
                    thresholds_by_suffix = {}

                    for col_name, clean_name in triplet:
                        #Sadiq Change
                        #feat_obj = model_features.get(clean_name)
                        feat_obj = model_features.get(col_name)

                        if not feat_obj:
                            continue
                        suffix = clean_name.rsplit('_', 1)[-1]
                        threshold = CVD_Risk_FeatureThresholds.objects.filter(
                            feature=feat_obj
                        ).values_list('threshold_value', flat=True).first()
                        if threshold is not None:
                            thresholds_by_suffix[suffix] = (col_name, threshold)
                            #Sadiq change
                            print("Thresholds,",thresholds_by_suffix)

                    # Infer missing thresholds if needed
                    try:
                        suffixes = thresholds_by_suffix.keys()
                        if 'Lower.third' in suffixes and 'Upper.third' in suffixes and 'Middle.third' not in suffixes:
                            lower_val = thresholds_by_suffix['Lower.third'][1]
                            upper_val = thresholds_by_suffix['Upper.third'][1]
                            middle_val = (lower_val + upper_val) / 2
                            middle_col = next((f for f in feature_order if f.endswith('_Middle.third') and base_name in f), None)
                            if middle_col:
                                thresholds_by_suffix['Middle.third'] = (middle_col, middle_val)
                        elif 'Lower.third' in suffixes and 'Middle.third' in suffixes and 'Upper.third' not in suffixes:
                            lower_val = thresholds_by_suffix['Lower.third'][1]
                            middle_val = thresholds_by_suffix['Middle.third'][1]
                            upper_val = 2 * middle_val - lower_val
                            upper_col = next((f for f in feature_order if f.endswith('_Upper.third') and base_name in f), None)
                            if upper_col:
                                thresholds_by_suffix['Upper.third'] = (upper_col, upper_val)
                        elif 'Middle.third' in suffixes and 'Upper.third' in suffixes and 'Lower.third' not in suffixes:
                            middle_val = thresholds_by_suffix['Middle.third'][1]
                            upper_val = thresholds_by_suffix['Upper.third'][1]
                            lower_val = 2 * middle_val - upper_val
                            lower_col = next((f for f in feature_order if f.endswith('_Lower.third') and base_name in f), None)
                            if lower_col:
                                thresholds_by_suffix['Lower.third'] = (lower_col, lower_val)
                    except Exception as e:
                        print(f"❌ Error inferring thresholds for {base_name}: {e}")

                    # Apply encoding
                    if 'Lower.third' in thresholds_by_suffix and val <= thresholds_by_suffix['Lower.third'][1]:
                        feature_values[thresholds_by_suffix['Lower.third'][0]] = 1
                    elif 'Middle.third' in thresholds_by_suffix and val <= thresholds_by_suffix['Middle.third'][1]:
                        feature_values[thresholds_by_suffix['Middle.third'][0]] = 1
                    elif 'Upper.third' in thresholds_by_suffix:
                        feature_values[thresholds_by_suffix['Upper.third'][0]] = 1
                else:
                    feature_values[fname] = float(val)

            # === B. Single-Select ===
            elif response.response_type == 'Select one answer':

                if response.option_selected:

                    selected_value = response.option_selected.encoded_value
                    feature_suffix = full_feature_name.split("_")[-1]

                    print("\n---- SINGLE SELECT DEBUG ----")
                    print("Feature:", full_feature_name)
                    print("Feature suffix:", feature_suffix)
                    print("Selected encoded value:", selected_value)

                    try:
                        if float(feature_suffix.replace("neg", "-")) == float(selected_value):
                            print("✅ MATCHED → setting 1")
                            feature_values[fname] = 1
                        else:
                            print("❌ No match")
                    except Exception as e:
                        print("❌ Comparison error:", e)


            # === C. Multi-Select ===
            elif response.response_type == 'Toggle multiple answer':

                selected_codes = [str(opt.encoded_value) for opt in response.multi_selected_options.all()]
                feature_code = full_feature_name.split("_")[-1]

                if "Gas.or.solid.fuel.cooking.heating" in full_feature_name:
                    print("\n==== MULTI-SELECT DEBUG (Gas/solid fuel) ====")
                    print("FEATURE:", full_feature_name)
                    print("FEATURE_CODE:", repr(feature_code))
                    print("SELECTED_CODES:", selected_codes)
                    print("SELECTED_CODES_REPR:", [repr(x) for x in selected_codes])
                    print("MATCH?", feature_code in selected_codes)

                if feature_code in selected_codes:
                    feature_values[fname] = 1
                try:
                    if float(feature_code.replace("neg", "-")) in [float(x) for x in selected_codes]:
                        print("✅ MATCHED MULTI → setting 1")
                        feature_values[fname] = 1
                except Exception as e:
                    print("❌ Multi compare error:", e)     

        except Exception as e:
            print(f"❌ Error processing feature {full_feature_name}: {e}")
            continue

    # 7. Save to DB — no transactions to avoid savepoint issues
    connections.close_all()
    saved_count = 0
    skipped_unmapped = 0
    timestamp = timezone.now()

    for fname, value in feature_values.items():
        #Sadiq change
        #full_feature_name = re.sub(r'^category_.*?_ts_', '', fname).strip()
        full_feature_name = fname

        if full_feature_name not in model_features:
            skipped_unmapped += 1
            continue

        feature_obj = model_features[full_feature_name]

        try:
            #connections.close_all()
            CVD_Risk_CalculatedFeatures.objects.update_or_create(
                patient_id=patient_id,
                model=model,
                feature=feature_obj,
                defaults={'value': value, 'created_at': timestamp}
            )
            saved_count += 1
        except Exception as e:
            print(f"❌ Error saving feature {full_feature_name} with value {value}: {e}")
            connections.close_all()
            continue

    print(f"⚠️ Skipped {skipped_unmapped} unmapped features (not present in model DB mappings)")
    print(f"✅ Saved or updated {saved_count} features for patient {patient_id}")

    # 8. Export for debugging
    try:
        df_out = pd.DataFrame([feature_values])
        os.makedirs("model_outputs", exist_ok=True)
        out_path = f"model_outputs/patient_{patient_id}_{model_name}_input.csv"
        df_out.to_csv(out_path, index=False)
        print(f"📁 CSV saved to: {out_path}")
    except Exception as e:
        print(f"❌ Failed to save CSV: {e}")

    print("\n================ RAW FEATURE VALUES ================\n")
    for k, v in feature_values.items():
        if v != 0:
            print(f"{k}: {v}")
    print("\n====================================================\n")

    return feature_values