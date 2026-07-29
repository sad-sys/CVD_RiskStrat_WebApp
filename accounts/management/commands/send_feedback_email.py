from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


class Command(BaseCommand):
    help = "Send one-week feedback emails"

    def handle(self, *args, **kwargs):

        # Only include users who joined at least 7 days ago
        cutoff_date = timezone.now() - timedelta(days=7)

        clinician_feedback_url = (
            settings.SITE_URL.rstrip("/")
            + reverse("clinician_feedback")
        )

        patient_feedback_url = (
            settings.SITE_URL.rstrip("/")
            + reverse("patient_feedback")
        )

        clinician_users = User.objects.filter(
            date_joined__lte=cutoff_date,
            one_week_email_sent=False,
            is_active=True,
            role="clinician_approved",
        )

        self.stdout.write(
            f"Found {clinician_users.count()} eligible clinicians"
        )

        for clinician in clinician_users:

            number_sent = send_mail(
                subject="PreciseCVD feedback form",
                message=(
                    f"Hi {clinician.first_name},\n\n"
                    "Thank you for using PreciseCVD.\n\n"
                    "Please complete our short clinician feedback form using "
                    "the link below:\n\n"
                    f"{clinician_feedback_url}\n\n"
                    "You may need to log in before completing the form.\n\n"
                    "Kind regards,\n"
                    "The PreciseCVD team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[clinician.email],
                fail_silently=False,
            )

            if number_sent == 1:
                clinician.one_week_email_sent = True
                clinician.save(
                    update_fields=["one_week_email_sent"]
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Sent clinician feedback email to "
                        f"{clinician.email}"
                    )
                )

        patient_users = User.objects.filter(
            date_joined__lte=cutoff_date,
            one_week_email_sent=False,
            is_active=True,
            role="patient",
        )

        self.stdout.write(
            f"Found {patient_users.count()} eligible patients"
        )

        for patient in patient_users:

            number_sent = send_mail(
                subject="PreciseCVD feedback form",
                message=(
                    f"Hi {patient.first_name},\n\n"
                    "Thank you for using PreciseCVD.\n\n"
                    "Please complete our short patient feedback form using "
                    "the link below:\n\n"
                    f"{patient_feedback_url}\n\n"
                    "You may need to log in before completing the form.\n\n"
                    "Kind regards,\n"
                    "The PreciseCVD team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient.email],
                fail_silently=False,
            )

            if number_sent == 1:
                patient.one_week_email_sent = True
                patient.save(
                    update_fields=["one_week_email_sent"]
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Sent patient feedback email to {patient.email}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Finished sending one-week feedback emails."
            )
        )