from django import forms
from .models import Users, Patients
from django.contrib.auth.forms import UserCreationForm
from .models import ClinicianFeedback, PatientFeedback


class CustomUserCreationForm(UserCreationForm):
    sex = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()

            # 🛡️ Check if patient already exists before creating
            if not hasattr(user, 'patients'):
                Patients.objects.create(user=user, sex=self.cleaned_data['sex'])
            else:
                # Optional update in case sex wasn't set
                user.patients.sex = self.cleaned_data['sex']
                user.patients.save()
            
        return user

class ClinicianFeedbackForm(forms.ModelForm):
    class Meta:
        model = ClinicianFeedback
        fields = ["rating"]
        labels = {
            "rating": "As a clinician, how much do you like this platform?",
        }
        widgets = {
            "rating": forms.RadioSelect,
        }


class PatientFeedbackForm(forms.ModelForm):

    class Meta:
        model = PatientFeedback

        fields = [
            "learned_about_platform",
            "learned_about_other",
            "platform_usage_count",
            "registration_ease",
            "instruction_clarity",
            "questionnaire_ease",
            "questionnaire_completion_time",
            "risk_report_ease",
            "risk_factor_explanation_usefulness",
            "risk_level_clarity",
            "understands_risk_score",
            "plans_to_discuss_results",
            "prediction_confidence",
            "liked_most",
            "confusing_or_difficult",
            "suggested_improvements",
            "additional_comments",
            "overall_satisfaction",
        ]

        labels = {
            "learned_about_platform":
                "1. How did you first learn about the PRECISE-CVD platform?",

            "learned_about_other":
                "Please specify how you learned about the platform",

            "platform_usage_count":
                "2. How many times have you used the platform?",

            "registration_ease":
                "3. How easy was it to register and log in to the platform?",

            "instruction_clarity":
                "4. How clear were the instructions provided on the platform?",

            "questionnaire_ease":
                "5. How easy was it to complete the health questionnaire?",

            "questionnaire_completion_time":
                "6. How long did it take you to complete the questionnaire?",

            "risk_report_ease":
                "7. How easy was it to understand your risk report?",

            "risk_factor_explanation_usefulness":
                "8. How useful were the explanations of your risk factors?",

            "risk_level_clarity":
                "9. How clearly did the report explain your risk level?",

            "understands_risk_score":
                "10. Do you understand what your risk score means?",

            "plans_to_discuss_results":
                "11. Do you plan to discuss your results with your GP or a specialist?",

            "prediction_confidence":
                "12. How confident are you in the risk prediction provided by the platform?",

            "liked_most":
                "13. What did you like most about the platform?",

            "confusing_or_difficult":
                "14. What did you find confusing or difficult to use?",

            "suggested_improvements":
                "15. What improvements would you suggest?",

            "additional_comments":
                "16. Any other comments or feedback?",

            "overall_satisfaction":
                "17. Overall, how satisfied are you with the PRECISE-CVD platform?",
        }

        widgets = {
            "learned_about_platform": forms.RadioSelect,
            "platform_usage_count": forms.RadioSelect,
            "registration_ease": forms.RadioSelect,
            "instruction_clarity": forms.RadioSelect,
            "questionnaire_ease": forms.RadioSelect,
            "questionnaire_completion_time": forms.RadioSelect,
            "risk_report_ease": forms.RadioSelect,
            "risk_factor_explanation_usefulness": forms.RadioSelect,
            "risk_level_clarity": forms.RadioSelect,
            "understands_risk_score": forms.RadioSelect,
            "plans_to_discuss_results": forms.RadioSelect,
            "prediction_confidence": forms.RadioSelect,
            "overall_satisfaction": forms.RadioSelect,

            "learned_about_other": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Please specify",
                }
            ),

            "liked_most": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter your answer",
                }
            ),

            "confusing_or_difficult": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter your answer",
                }
            ),

            "suggested_improvements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter your answer",
                }
            ),

            "additional_comments": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter your answer",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        learned_about = cleaned_data.get("learned_about_platform")
        learned_about_other = cleaned_data.get("learned_about_other")

        if learned_about == "other" and not learned_about_other:
            self.add_error(
                "learned_about_other",
                "Please specify how you learned about the platform.",
            )

        return cleaned_data