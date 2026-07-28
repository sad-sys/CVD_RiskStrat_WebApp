from django.contrib import admin, messages
from django.conf import settings
from django.core.mail import send_mail

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

    clinician_form_url = (
        "https://forms.office.com/Pages/DesignPageV2.aspx"
        "?subpage=design"
        "&FormId=FM9wg_MWFky4PHJAcWVDVmI-smpi4FtBkad56uUvX6NUOElXUTdJQVZFUFhLNUxHUUdJUURWWU82NS4u"
        "&Token=b277f6b5e72d429e9ca568fc61c1c293"
    )

    patient_form_url = (
        "https://forms.cloud.microsoft/Pages/DesignPageV2.aspx"
        "?subpage=design"
        "&FormId=FM9wg_MWFky4PHJAcWVDVmI-smpi4FtBkad56uUvX6NUN0lHM1FQTDhOU1ZIT1dTTUhLRE1LRjZTQi4u"
        "&Token=9c2a4a48b1ea48d583ba8cb8b0e53be7"
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
            greeting = "Dear clinician,"

        elif user.role == "patient":
            form_url = patient_form_url
            greeting = "Dear participant,"

        else:
            skipped_count += 1
            continue

        email_message = (
            f"{greeting}\n\n"
            "Thank you for using PreciseCVD.\n\n"
            "We would be grateful if you could complete our short feedback form:\n\n"
            f"{form_url}\n\n"
            "Your feedback will help us improve the platform.\n\n"
            "Kind regards,\n"
            "The PreciseCVD Team"
        )

        try:
            send_mail(
                subject="PreciseCVD feedback form",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Record that the feedback email has been sent
            user.one_week_email_sent = True
            user.save(update_fields=["one_week_email_sent"])

            sent_count += 1

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