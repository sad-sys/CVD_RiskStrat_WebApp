import pandas as pd
from accounts.models import (
    CVD_Risk_Model_InputFeatures,
    CVD_risk_Questionnaire,
    CVD_risk_QuestionResponseOptions
)

def run():
    df = pd.read_excel("/Users/sadiqkhawaja/Desktop/SociodemographicsMapping.xlsx")

    instance_to_question_text = dict(zip(df.iloc[:, 0], df.iloc[:, 8]))
    instance_to_option_text = dict(zip(df.iloc[:, 0], df.iloc[:, 9]))

    linked = 0

    for feature in CVD_Risk_Model_InputFeatures.objects.filter(question__isnull=True):

        if "_ts_" not in feature.feature_name:
            continue

        instance_part = feature.feature_name.split("_ts_")[1]

        if instance_part in instance_to_question_text:

            question_text = instance_to_question_text[instance_part]
            option_text = instance_to_option_text.get(instance_part)

            try:
                question = CVD_risk_Questionnaire.objects.get(question_text=question_text)
                feature.question = question

                if isinstance(option_text, str) and option_text.strip():
                    option = CVD_risk_QuestionResponseOptions.objects.filter(
                        question=question,
                        option_text=option_text
                    ).first()
                    feature.encoded_option = option

                feature.save()
                linked += 1
                print("Linked:", feature.feature_name)

            except Exception as e:
                print("Failed:", feature.feature_name, e)

    print("Total linked:", linked)
