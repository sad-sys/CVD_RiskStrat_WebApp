import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import CVD_ModelFeatureMappings, CVD_risk_Questionnaire, ML_Models

model = ML_Models.objects.get(model_name="MRMR_COX_Sociodemographics")

def link_feature(feature_name, question_id):
    q = CVD_risk_Questionnaire.objects.get(question_id=question_id)
    m = CVD_ModelFeatureMappings.objects.get(
        model=model,
        input_feature__feature_name=feature_name
    )
    m.input_feature.question = q
    m.input_feature.save()
    print(f"Linked: {feature_name} → {question_id}")


# 1️⃣ Type of accommodation _5
link_feature(
    "category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_5",
    670
)

# 2️⃣ Heavy manual work _1
link_feature(
    "category_Sociodemographics_ts_Job.involves.heavy.manual.or.physical.work...Instance.0_1",
    816
)

# 3️⃣ Heavy manual work _2
link_feature(
    "category_Sociodemographics_ts_Job.involves.heavy.manual.or.physical.work...Instance.0_2",
    816
)

# 4️⃣ Age completed education _neg2
link_feature(
    "category_Sociodemographics_ts_Age.completed.full.time.education...Instance.0_neg2",
    845
)

# 5️⃣ Year immigrated Upper third
link_feature(
    "category_Sociodemographics_ts_Year.immigrated.to.UK..United.Kingdom....Instance.0_Upper.third",
    3659
)
