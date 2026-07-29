from django.contrib import admin, messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .models import (
    Patients,
    Clinicians,
    CVD_risk_Clinician_Patient,
    Users,
    CVD_risk_Questionnaire,
    CVD_risk_QuestionResponseOptions,
    CVD_risk_Responses,
    CVD_risk_Patient_Outcomes,
    Risk_Stratification,
    ML_Models,
    batch_CVD_Risk_Features,
    batch_CVD_Risk_Model_Features,
    batch_CVD_Risk_Risk,
    batch_CVD_Risk_Output,
    ClinicianAccessRequest,
)


# ============================================================
# FEEDBACK EMAIL ADMIN ACTION
# ============================================================

@admin.action(description="Send PreciseCVD feedback email")
def send_feedback_email(modeladmin, request, queryset):

    clinician_form_url = request.build_absolute_uri(
        reverse("clinician_feedback")
    )

    patient_form_url = request.build_absolute_uri(
        reverse("patient_feedback")
    )

    sent_count = 0
    skipped_count = 0
    failed_count = 0

    for user in queryset:

        # Skip users who cannot receive an email
        if not user.is_active or not user.email:
            skipped_count += 1
            continue

        # Choose the correct form based on role
        if user.role == "clinician_approved":
            form_url = clinician_form_url
            greeting = f"Dear {user.first_name or 'clinician'},"

        elif user.role == "patient":
            form_url = patient_form_url
            greeting = f"Dear {user.first_name or 'participant'},"

        else:
            skipped_count += 1
            continue

        email_message = (
            f"{greeting}\n\n"
            "Thank you for using PreciseCVD.\n\n"
            "We would be grateful if you could complete our short "
            "feedback form using the link below:\n\n"
            f"{form_url}\n\n"
            "You may need to log in before completing the form.\n\n"
            "Your feedback will help us improve the platform.\n\n"
            "Kind regards,\n"
            "The PreciseCVD Team"
        )

        try:
            number_sent = send_mail(
                subject="PreciseCVD feedback form",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            if number_sent == 1:
                sent_count += 1
            else:
                failed_count += 1

                modeladmin.message_user(
                    request,
                    f"The email to {user.email} was not sent.",
                    level=messages.ERROR,
                )

        except Exception as error:
            failed_count += 1

            modeladmin.message_user(
                request,
                f"Failed to send feedback email to {user.email}: {error}",
                level=messages.ERROR,
            )

    # Show a summary inside Django Admin
    if sent_count > 0:
        modeladmin.message_user(
            request,
            f"Successfully sent {sent_count} feedback email(s).",
            level=messages.SUCCESS,
        )

    if skipped_count > 0:
        modeladmin.message_user(
            request,
            (
                f"Skipped {skipped_count} user(s). "
                "They were inactive, had no email address, "
                "or did not have a supported role."
            ),
            level=messages.WARNING,
        )

    if failed_count > 0:
        modeladmin.message_user(
            request,
            f"{failed_count} feedback email(s) failed to send.",
            level=messages.ERROR,
        )
# ============================================================
# USERS ADMIN
# ============================================================

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "role",
        "is_active",
        "date_joined",
        "one_week_email_sent",
    )

    list_filter = (
        "role",
        "is_active",
        "one_week_email_sent",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    ordering = (
        "-date_joined",
    )

    actions = [
        send_feedback_email,
    ]


# ============================================================
# OTHER MODELS
# ============================================================

admin.site.register(Patients)
admin.site.register(Clinicians)
admin.site.register(CVD_risk_Clinician_Patient)
admin.site.register(CVD_risk_Questionnaire)
admin.site.register(CVD_risk_QuestionResponseOptions)
admin.site.register(CVD_risk_Responses)
admin.site.register(CVD_risk_Patient_Outcomes)
admin.site.register(Risk_Stratification)
admin.site.register(ML_Models)
admin.site.register(batch_CVD_Risk_Features)
admin.site.register(batch_CVD_Risk_Model_Features)
admin.site.register(batch_CVD_Risk_Risk)
admin.site.register(batch_CVD_Risk_Output)
admin.site.register(ClinicianAccessRequest)
from django.contrib import admin
from .models import PatientFeedback, ClinicianFeedback

admin.site.register(PatientFeedback)
admin.site.register(ClinicianFeedback)