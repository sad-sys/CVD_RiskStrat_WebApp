import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
print("Starting...")
django.setup()
print("Django setup complete")

from accounts.models import (
    CVD_Risk_Model_InputFeatures,
    CVD_Risk_FeatureThresholds
)

# Only define lower & upper once per base variable
base_thresholds = {
    "Age.heart.attack.diagnosed...Instance.0": (50, 57),
    "Age.angina.diagnosed...Instance.0": (50, 58),
    "Age.stroke.diagnosed...Instance.0": (51, 59),
    "Age.high.blood.pressure.diagnosed...Instance.0": (48, 56),
    "Time.since.last.prostate.specific.antigen..PSA..test...Instance.0": (1, 2),
    "Age.deep.vein.thrombosis..DVT..blood.clot.in.leg..diagnosed...Instance.0": (35, 51),
    "Age.pulmonary.embolism..blood.clot.in.lung..diagnosed...Instance.0": (40, 54),
    "Age.emphysema.chronic.bronchitis.diagnosed...Instance.0": (40, 55),
    "Age.asthma.diagnosed...Instance.0": (20, 42),
    "Age.hay.fever..rhinitis.or.eczema.diagnosed...Instance.0": (15, 30),
    "Age.diabetes.diagnosed...Instance.0": (50, 58),
}

for base_name, (lower, upper) in base_thresholds.items():

    lower_feature = f"category_Health and medical history_ts_{base_name}_Lower.third"
    middle_feature = f"category_Health and medical history_ts_{base_name}_Middle.third"
    upper_feature = f"category_Health and medical history_ts_{base_name}_Upper.third"

    for feature_name, threshold_value in [
        (lower_feature, lower),
        (middle_feature, upper),  # Middle uses upper boundary
        (upper_feature, upper),
    ]:

        try:
            feature = CVD_Risk_Model_InputFeatures.objects.get(
                feature_name=feature_name
            )
        except:
            print("⚠ Feature not found:", feature_name)
            continue

        CVD_Risk_FeatureThresholds.objects.update_or_create(
            feature_id=feature.feature_id,
            defaults={"threshold_value": threshold_value}
        )

        print("Uploaded:", feature_name, "→", threshold_value)

print("All HMH tertile thresholds uploaded correctly.")