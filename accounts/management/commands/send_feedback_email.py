from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = "Send one-week feedback emails"

    def handle(self, *args, **kwargs):

        cutoff_date = timezone.now() - timedelta(days=7)

        clinicianUsers = User.objects.filter(
            date_joined__lte=cutoff_date,
            one_week_email_sent=False,
            is_active=True,
            role="clinician_approved",
        )

        print(f"Found clinician {clinicianUsers.count()} clinicianUsers")

        for clinicianUser in clinicianUsers:

            send_mail(
                subject="PreciseCVD feedback form",
                message="Hi! Please complete our feedback form https://forms.office.com/Pages/DesignPageV2.aspx?subpage=design&FormId=FM9wg_MWFky4PHJAcWVDVmI-smpi4FtBkad56uUvX6NUOElXUTdJQVZFUFhLNUxHUUdJUURWWU82NS4u&Token=b277f6b5e72d429e9ca568fc61c1c293",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[clinicianUser.email],
                fail_silently=False,
            )

            clinicianUser.one_week_email_sent = True
            clinicianUser.save(update_fields=["one_week_email_sent"])

            print(f"Sent to {clinicianUser.email}")

        patientUsers = User.objects.filter(
        date_joined__lte=cutoff_date,
        one_week_email_sent=False,
        is_active=True,
        role="patient",
        )

        for patient in patientUsers:

            send_mail(
                subject="PreciseCVD feedback form",
                message="Hi! Please complete our feedback form https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?subpage=design&FormId=FM9wg_MWFky4PHJAcWVDVmI-smpi4FtBkad56uUvX6NUN0lHM1FQTDhOU1ZIT1dTTUhLRE1LRjZTQi4u&Token=9c2a4a48b1ea48d583ba8cb8b0e53be7",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient.email],
                fail_silently=False,
            )

            patient.one_week_email_sent = True
            patient.save(update_fields=["one_week_email_sent"])

            print(f"Sent to {patient.email}")

        