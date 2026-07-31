from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        # Set username to email if not provided
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
    
    #  Important: This ensures MySQL ENUM doesn't complain
        extra_fields.setdefault('role', 'clinician_approved')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # Required for access to admin
    is_superuser = models.BooleanField(default=True)  # Required for superuser privileges

    one_week_email_sent = models.BooleanField(default=False)
    
    def get_username(self):
        return self.email
    role = models.CharField(
        max_length=20,
        choices=[
            ('patient', 'Patient'),
            ('clinician_pending', 'Clinician Pending'),
            ('clinician_approved', 'Clinician Approved')
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    #  Plug in the custom manager here
    objects = CustomUserManager()

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'

from django.conf import settings
from django.db import models


class ClinicianFeedback(models.Model):

    # ========================================================
    # SECTION A: BACKGROUND INFORMATION
    # ========================================================

    EXPERIENCE_CHOICES = [
        ("under_2", "Less than 2 years"),
        ("2_to_5", "2–5 years"),
        ("6_to_10", "6–10 years"),
        ("11_to_20", "11–20 years"),
        ("over_20", "More than 20 years"),
    ]

    USAGE_COUNT_CHOICES = [
        ("first_time", "This is my first time"),
        ("2_to_5", "2–5 times"),
        ("6_to_10", "6–10 times"),
        ("over_10", "More than 10 times"),
    ]

    SETTING_CHOICES = [
        ("research", "Research"),
        ("clinical", "Clinical (patient-facing)"),
        ("both", "Both"),
        ("not_applicable", "Not applicable"),
    ]

    PRIOR_FAMILIARITY_CHOICES = [
        (
            "regular_user",
            "Yes, I use them regularly",
        ),
        (
            "aware_not_user",
            "Yes, I am aware of them but do not use them",
        ),
        (
            "not_familiar",
            "No, I was not familiar with them",
        ),
    ]

    # ========================================================
    # SHARED 1–5 SCALES
    # ========================================================

    EASE_CHOICES = [
        (1, "1 = Very difficult"),
        (2, "2 = Difficult"),
        (3, "3 = Neutral"),
        (4, "4 = Easy"),
        (5, "5 = Very easy"),
    ]

    CLARITY_CHOICES = [
        (1, "1 = Very unclear"),
        (2, "2 = Unclear"),
        (3, "3 = Neutral"),
        (4, "4 = Clear"),
        (5, "5 = Very clear"),
    ]

    INTUITIVENESS_CHOICES = [
        (1, "1 = Not at all intuitive"),
        (2, "2 = Slightly intuitive"),
        (3, "3 = Neutral"),
        (4, "4 = Intuitive"),
        (5, "5 = Very intuitive"),
    ]

    DESIGN_CHOICES = [
        (1, "1 = Very poor"),
        (2, "2 = Poor"),
        (3, "3 = Neutral"),
        (4, "4 = Good"),
        (5, "5 = Excellent"),
    ]

    SPEED_CHOICES = [
        (1, "1 = Very slow"),
        (2, "2 = Slow"),
        (3, "3 = Neutral"),
        (4, "4 = Fast"),
        (5, "5 = Very fast"),
    ]

    AGREEMENT_CHOICES = [
        (1, "1 = Strongly disagree"),
        (2, "2 = Disagree"),
        (3, "3 = Neutral"),
        (4, "4 = Agree"),
        (5, "5 = Strongly agree"),
    ]

    UNDERSTANDABILITY_CHOICES = [
        (1, "1 = Very confusing"),
        (2, "2 = Confusing"),
        (3, "3 = Neutral"),
        (4, "4 = Understandable"),
        (5, "5 = Very understandable"),
    ]

    USEFULNESS_CHOICES = [
        (1, "1 = Not useful"),
        (2, "2 = Slightly useful"),
        (3, "3 = Neutral"),
        (4, "4 = Useful"),
        (5, "5 = Very useful"),
    ]

    CONFIDENCE_CHOICES = [
        (1, "1 = No confidence"),
        (2, "2 = Little confidence"),
        (3, "3 = Neutral"),
        (4, "4 = Moderate confidence"),
        (5, "5 = High confidence"),
    ]

    LIKELIHOOD_CHOICES = [
        (1, "1 = Very unlikely"),
        (2, "2 = Unlikely"),
        (3, "3 = Neutral"),
        (4, "4 = Likely"),
        (5, "5 = Very likely"),
    ]

    RELEVANCE_CHOICES = [
        (1, "1 = Not relevant"),
        (2, "2 = Slightly relevant"),
        (3, "3 = Neutral"),
        (4, "4 = Relevant"),
        (5, "5 = Highly relevant"),
    ]

    SATISFACTION_CHOICES = [
        (1, "1 = Very dissatisfied"),
        (2, "2 = Dissatisfied"),
        (3, "3 = Neutral"),
        (4, "4 = Satisfied"),
        (5, "5 = Very satisfied"),
    ]

    # ========================================================
    # USER
    # ========================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clinician_feedbacks",
    )

    # ========================================================
    # SECTION A: BACKGROUND INFORMATION
    # ========================================================

    primary_clinical_role = models.CharField(
        max_length=150,
    )

    years_of_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
    )

    platform_usage_count = models.CharField(
        max_length=20,
        choices=USAGE_COUNT_CHOICES,
    )

    primary_use_setting = models.CharField(
        max_length=20,
        choices=SETTING_CHOICES,
    )

    prior_risk_model_familiarity = models.CharField(
        max_length=30,
        choices=PRIOR_FAMILIARITY_CHOICES,
    )

    # ========================================================
    # SECTION B: INTERFACE AND USABILITY
    # ========================================================

    navigation_ease = models.PositiveSmallIntegerField(
        choices=EASE_CHOICES,
    )

    instruction_clarity = models.PositiveSmallIntegerField(
        choices=CLARITY_CHOICES,
    )

    data_entry_intuitiveness = models.PositiveSmallIntegerField(
        choices=INTUITIVENESS_CHOICES,
    )

    visual_design_rating = models.PositiveSmallIntegerField(
        choices=DESIGN_CHOICES,
    )

    prediction_generation_speed = models.PositiveSmallIntegerField(
        choices=SPEED_CHOICES,
    )

    clear_action_feedback = models.PositiveSmallIntegerField(
        choices=AGREEMENT_CHOICES,
    )

    prediction_understandability = models.PositiveSmallIntegerField(
        choices=UNDERSTANDABILITY_CHOICES,
    )

    feature_importance_usefulness = models.PositiveSmallIntegerField(
        choices=USEFULNESS_CHOICES,
    )

    # ========================================================
    # SECTION C: TRUST AND CLINICAL RELEVANCE
    # ========================================================

    prediction_confidence = models.PositiveSmallIntegerField(
        choices=CONFIDENCE_CHOICES,
    )

    research_recommendation_likelihood = models.PositiveSmallIntegerField(
        choices=LIKELIHOOD_CHOICES,
    )

    clinical_output_relevance = models.PositiveSmallIntegerField(
        choices=RELEVANCE_CHOICES,
    )

    alignment_with_clinical_judgement = models.PositiveSmallIntegerField(
        choices=AGREEMENT_CHOICES,
    )

    trust_for_preventative_treatment = models.PositiveSmallIntegerField(
        choices=AGREEMENT_CHOICES,
    )

    # ========================================================
    # SECTION D: OPEN-ENDED FEEDBACK
    # ========================================================

    least_useful_feature = models.TextField(
        blank=True,
    )

    suggested_interface_improvements = models.TextField(
        blank=True,
    )

    requested_features = models.TextField(
        blank=True,
    )

    additional_comments = models.TextField(
        blank=True,
    )

    # ========================================================
    # SECTION E: SATISFACTION
    # ========================================================

    overall_satisfaction = models.PositiveSmallIntegerField(
        choices=SATISFACTION_CHOICES,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "clinician_feedback"
        ordering = ["-submitted_at"]

    def __str__(self):
        return (
            f"Clinician feedback from {self.user.email} "
            f"on {self.submitted_at:%d %b %Y}"
        )


class PatientFeedback(models.Model):

    # ========================================================
    # SECTION A: BACKGROUND INFORMATION
    # ========================================================

    LEARNED_ABOUT_CHOICES = [
        ("gp", "From my GP / doctor"),
        ("cardiologist", "From a specialist (cardiologist)"),
        ("research", "From a research study invitation"),
        ("family_friend", "From a family member or friend"),
        ("social_media", "From social media or online search"),
        ("other", "Other"),
    ]

    USAGE_COUNT_CHOICES = [
        ("first_time", "This is my first time"),
        ("2_to_5", "2–5 times"),
        ("more_than_5", "More than 5 times"),
    ]

    # ========================================================
    # SHARED 1–5 SCALES
    # ========================================================

    DIFFICULTY_CHOICES = [
        (1, "1 = Very difficult"),
        (2, "2 = Difficult"),
        (3, "3 = Neutral"),
        (4, "4 = Easy"),
        (5, "5 = Very easy"),
    ]

    CLARITY_CHOICES = [
        (1, "1 = Very unclear"),
        (2, "2 = Unclear"),
        (3, "3 = Neutral"),
        (4, "4 = Clear"),
        (5, "5 = Very clear"),
    ]

    USEFULNESS_CHOICES = [
        (1, "1 = Not useful"),
        (2, "2 = Slightly useful"),
        (3, "3 = Neutral"),
        (4, "4 = Useful"),
        (5, "5 = Very useful"),
    ]

    CONFIDENCE_CHOICES = [
        (1, "1 = Not confident"),
        (2, "2 = Slightly confident"),
        (3, "3 = Neutral"),
        (4, "4 = Confident"),
        (5, "5 = Very confident"),
    ]

    SATISFACTION_CHOICES = [
        (1, "1 = Very dissatisfied"),
        (2, "2 = Dissatisfied"),
        (3, "3 = Neutral"),
        (4, "4 = Satisfied"),
        (5, "5 = Very satisfied"),
    ]

    COMPLETION_TIME_CHOICES = [
        ("under_5", "Less than 5 minutes"),
        ("5_to_10", "5–10 minutes"),
        ("10_to_15", "10–15 minutes"),
        ("15_to_20", "15–20 minutes"),
        ("over_20", "More than 20 minutes"),
    ]

    UNDERSTANDING_CHOICES = [
        ("no", "No, not at all"),
        ("somewhat", "Yes, somewhat"),
        ("well", "Yes, I understand it well"),
    ]

    DISCUSSION_CHOICES = [
        ("no", "No"),
        ("yes", "Yes"),
        ("unsure", "Not sure"),
    ]

    # ========================================================
    # USER
    # ========================================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_feedbacks",
    )

    # ========================================================
    # SECTION A: BACKGROUND INFORMATION
    # ========================================================

    learned_about_platform = models.CharField(
        max_length=30,
        choices=LEARNED_ABOUT_CHOICES,
    )

    learned_about_other = models.CharField(
        max_length=255,
        blank=True,
    )

    platform_usage_count = models.CharField(
        max_length=20,
        choices=USAGE_COUNT_CHOICES,
    )

    # ========================================================
    # SECTION B: PLATFORM USABILITY
    # ========================================================

    registration_ease = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
    )

    instruction_clarity = models.PositiveSmallIntegerField(
        choices=CLARITY_CHOICES,
    )

    questionnaire_ease = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
    )

    questionnaire_completion_time = models.CharField(
        max_length=20,
        choices=COMPLETION_TIME_CHOICES,
    )

    risk_report_ease = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
    )

    risk_factor_explanation_usefulness = models.PositiveSmallIntegerField(
        choices=USEFULNESS_CHOICES,
    )

    # ========================================================
    # SECTION C: UNDERSTANDING AND TRUST
    # ========================================================

    risk_level_clarity = models.PositiveSmallIntegerField(
        choices=CLARITY_CHOICES,
    )

    understands_risk_score = models.CharField(
        max_length=20,
        choices=UNDERSTANDING_CHOICES,
    )

    plans_to_discuss_results = models.CharField(
        max_length=10,
        choices=DISCUSSION_CHOICES,
    )

    prediction_confidence = models.PositiveSmallIntegerField(
        choices=CONFIDENCE_CHOICES,
    )

    # ========================================================
    # SECTION D: OPEN FEEDBACK
    # ========================================================

    liked_most = models.TextField(
        blank=True,
    )

    confusing_or_difficult = models.TextField(
        blank=True,
    )

    suggested_improvements = models.TextField(
        blank=True,
    )

    additional_comments = models.TextField(
        blank=True,
    )

    # ========================================================
    # SECTION E: OVERALL SATISFACTION
    # ========================================================

    overall_satisfaction = models.PositiveSmallIntegerField(
        choices=SATISFACTION_CHOICES,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "patient_feedback"
        ordering = ["-submitted_at"]

    def __str__(self):
        return (
            f"Patient feedback from {self.user.email} "
            f"on {self.submitted_at:%d %b %Y}"
        )


class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    clinician = models.ForeignKey('Clinicians', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Patients'
        verbose_name_plural = 'Patients'


class Clinicians(models.Model):
    clinician_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Clinicians'
        verbose_name_plural = 'Clinicians'


class CVD_risk_Questionnaire(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    subcategory = models.CharField(max_length=100, null=True, blank=True)
    question_order = models.IntegerField(default=0)
    answer_type = models.CharField(max_length=50, null=True, blank=True)    

    class Meta:
        db_table = 'CVD_risk_Questionnaire'
        verbose_name_plural = 'CVD Risk Questionnaire'
        

class CVD_risk_QuestionnaireDependency(models.Model):
    triggering_question = models.ForeignKey(
        'CVD_risk_Questionnaire', related_name='dependent_questions', on_delete=models.CASCADE
    )
    conditional_question = models.ForeignKey(
        'CVD_risk_Questionnaire', related_name='trigger_questions', on_delete=models.CASCADE
    )
    trigger_values = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"If Q{self.triggering_question.question_id} in {self.trigger_values} ⇒ show Q{self.conditional_question.question_id}"

    class Meta:
        db_table = 'CVD_risk_Questionnaire_dependency_values'
        verbose_name = "Question Dependency"
        verbose_name_plural = "Question Dependencies"
        unique_together = ('triggering_question', 'conditional_question')  # Optional constraint


class CVD_risk_QuestionResponseOptions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(CVD_risk_Questionnaire, on_delete=models.CASCADE)
    option_text = models.TextField()
    encoded_value = models.FloatField(null=True, blank=True)
    option_label = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'CVD_risk_QuestionResponseOptions'
        verbose_name_plural = 'Questionnaire Response Options'


class CVD_risk_Responses(models.Model):
    response_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    question = models.ForeignKey(CVD_risk_Questionnaire, on_delete=models.CASCADE)
    response_type = models.CharField(max_length=50)
    numeric_response = models.FloatField(null=True, blank=True)
    boolean_response = models.BooleanField(null=True, blank=True)
    option_selected = models.ForeignKey(CVD_risk_QuestionResponseOptions, on_delete=models.SET_NULL, null=True, blank=True)
    multi_selected_options = models.ManyToManyField(CVD_risk_QuestionResponseOptions, related_name="multi_responses", blank=True)
    response_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    submission_id = models.CharField(max_length=100, null=True, blank=True)

    @property
    def encoded_single_option(self):
        """Returns encoded value of selected option if applicable."""
        return self.option_selected.encoded_value if self.option_selected else None
    @property
    def encoded_multi_options(self):
        """Returns list of encoded values from multi-selected options."""
        return [opt.encoded_value for opt in self.multi_selected_options.all()]

    class Meta:
        db_table = 'CVD_risk_Responses'
        verbose_name_plural = 'CVD Risk Responses'

class ClinicianPermissions(models.Model):
    clinician = models.OneToOneField(Clinicians, on_delete=models.CASCADE, related_name='permissions')
    can_access_cvd = models.BooleanField(default=True)
    can_access_tavi = models.BooleanField(default=True)

    class Meta:
        db_table = 'Clinician_Permissions'
        verbose_name_plural = 'Clinician Permissions'

    def __str__(self):
        return f"{self.clinician.user.email} — CVD: {self.can_access_cvd}, TAVI: {self.can_access_tavi}"


class FeatureOptionMapping(models.Model):
    feature_name = models.CharField(max_length=300)
    question = models.ForeignKey(CVD_risk_Questionnaire, on_delete=models.CASCADE)
    option = models.ForeignKey(CVD_risk_QuestionResponseOptions, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('feature_name', 'question')
        db_table = 'Feature_Option_Mappings'
        verbose_name_plural = "Feature Option Mappings"

    def __str__(self):
        return f"{self.feature_name} → {self.option.option_text}"
        


class CVD_risk_Clinician_Patient(models.Model):
    id = models.AutoField(primary_key=True)
    clinician = models.ForeignKey(Clinicians, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CVD_risk_Clinician_Patient'
        verbose_name_plural = 'Clinician Patients'


class ML_Models(models.Model):
    model_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=100)

    class Meta:
        db_table = 'ML_Models'
        verbose_name_plural = 'ML Models'

class CVD_Risk_Model_InputFeatures(models.Model):
    feature_id = models.AutoField(primary_key=True)

    question = models.ForeignKey(
        CVD_risk_Questionnaire,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    feature_name = models.CharField(
        max_length=255,
        unique=True   # ← important
    )

    encoded_option = models.ForeignKey(
        CVD_risk_QuestionResponseOptions,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )



class CVD_Risk_CalculatedFeatures(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    model = models.ForeignKey(ML_Models, on_delete=models.CASCADE)
    feature = models.ForeignKey(CVD_Risk_Model_InputFeatures, on_delete=models.CASCADE)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CVD_Risk_CalculatedFeatures'
        verbose_name_plural = 'CVD Risk Calculated Features'
        unique_together = ('patient', 'model', 'feature')

        

class CVD_ModelFeatureMappings(models.Model):
    model = models.ForeignKey(ML_Models, on_delete=models.CASCADE)
    input_feature = models.ForeignKey(CVD_Risk_Model_InputFeatures, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CVD_ModelFeatureMappings'
        verbose_name_plural = 'Model Feature Mappings'
        unique_together = (('model', 'input_feature'),)
        

class CVD_Risk_FeatureThresholds(models.Model):
    feature = models.ForeignKey(CVD_Risk_Model_InputFeatures, on_delete=models.CASCADE)
    threshold_value = models.FloatField()

    class Meta:
        db_table = 'CVD_Risk_FeatureThresholds'
        verbose_name_plural = 'CVD Risk Feature Thresholds'
        unique_together = (('feature',),)



class Risk_Stratification(models.Model):
    stratification_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)
    recommendation = models.TextField()
    assessed_at = models.DateTimeField(auto_now_add=True)
    model = models.ForeignKey(ML_Models, on_delete=models.SET_NULL, null=True)
    submission_id = models.CharField(max_length=100, null=True, blank=True)  # NEW
    alert_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'Risk_Stratification'
        verbose_name_plural = 'Risk Stratification'


class CVD_risk_Patient_Outcomes(models.Model):
    outcome_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    outcome_description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CVD_risk_Patient_Outcomes'
        verbose_name_plural = 'CVD Risk Patient Outcomes'

class batch_CVD_Risk_Features(models.Model):
    feature_id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=255)
    feature_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'batch_CVD_Risk_Features'
        verbose_name_plural = 'Batch CVD Risk Features'


class batch_CVD_Risk_Model_Features(models.Model):
    model = models.ForeignKey(ML_Models, on_delete=models.CASCADE)
    feature = models.ForeignKey(batch_CVD_Risk_Features, on_delete=models.CASCADE)

    class Meta:
        db_table = 'batch_CVD_Risk_Model_Features'
        unique_together = (('model', 'feature'),)
        verbose_name_plural = 'Batch CVD Risk Model Features'


class batch_CVD_Risk_Risk(models.Model):
    risk_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    model = models.ForeignKey(ML_Models, on_delete=models.CASCADE)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)
    prediction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'batch_CVD_Risk_Risk'
        verbose_name_plural = 'Batch CVD Risk Risk'


class batch_CVD_Risk_Output(models.Model):
    output_id = models.AutoField(primary_key=True)
    risk = models.ForeignKey(batch_CVD_Risk_Risk, on_delete=models.CASCADE)
    plot_type = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'batch_CVD_Risk_Output'
        verbose_name_plural = 'Batch CVD Risk Output'


class ClinicianAccessRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clinician_access_requests',
        null =True, #temporary
        blank=True
        )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=255)
    reason = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    password_hash = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) - {self.status}";
    class Meta:
        db_table = 'Clinician_Access_Request'
        verbose_name_plural = 'Clinician Access Requests'
