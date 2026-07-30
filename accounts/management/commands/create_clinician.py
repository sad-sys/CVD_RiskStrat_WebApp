from django.core.management.base import BaseCommand, CommandError

from accounts.models import Users, Clinicians


class Command(BaseCommand):
    help = "Create a new approved clinician account or update an existing user."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            required=True,
            help="Email address for the clinician.",
        )

        parser.add_argument(
            "--first-name",
            default="",
            help="Clinician's first name.",
        )

        parser.add_argument(
            "--last-name",
            default="",
            help="Clinician's last name.",
        )

        parser.add_argument(
            "--password",
            help=(
                "Password for a newly created user. "
                "If omitted, the new account will have an unusable password."
            ),
        )

        parser.add_argument(
            "--specialty",
            default=None,
            help="Clinician specialty.",
        )

    def handle(self, *args, **options):
        email = options["email"].strip().lower()
        first_name = options["first_name"].strip()
        last_name = options["last_name"].strip()
        password = options.get("password")
        specialty = options.get("specialty")

        if not email:
            raise CommandError("A valid email address is required.")

        user, user_created = Users.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": "clinician_approved",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        )

        if user_created:
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()

            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created user account: {user.email}"
                )
            )

        else:
            updated_fields = []

            if first_name and user.first_name != first_name:
                user.first_name = first_name
                updated_fields.append("first_name")

            if last_name and user.last_name != last_name:
                user.last_name = last_name
                updated_fields.append("last_name")

            if user.role != "clinician_approved":
                user.role = "clinician_approved"
                updated_fields.append("role")

            if not user.is_active:
                user.is_active = True
                updated_fields.append("is_active")

            if user.is_staff:
                user.is_staff = False
                updated_fields.append("is_staff")

            if user.is_superuser:
                user.is_superuser = False
                updated_fields.append("is_superuser")

            if password:
                user.set_password(password)
                updated_fields.append("password")

            if updated_fields:
                user.save(update_fields=updated_fields)

                self.stdout.write(
                    self.style.WARNING(
                        f"Updated existing user: {user.email}"
                    )
                )
            else:
                self.stdout.write(
                    f"User already configured correctly: {user.email}"
                )

        clinician, clinician_created = Clinicians.objects.get_or_create(
            user=user,
            defaults={
                "specialty": specialty,
            },
        )

        if not clinician_created and specialty is not None:
            clinician.specialty = specialty
            clinician.save(update_fields=["specialty"])

        if clinician_created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created linked clinician profile."
                )
            )
        else:
            self.stdout.write(
                "Linked clinician profile already exists."
            )

        user.refresh_from_db()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Clinician setup complete"))
        self.stdout.write(f"Email: {user.email}")
        self.stdout.write(f"Role: {user.role}")
        self.stdout.write(f"Active: {user.is_active}")
        self.stdout.write(f"Staff: {user.is_staff}")
        self.stdout.write(f"Superuser: {user.is_superuser}")
        self.stdout.write(
            f"Clinician profile: "
            f"{Clinicians.objects.filter(user=user).exists()}"
        )