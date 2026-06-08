import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import (
    ML_Models,
    CVD_Risk_Model_InputFeatures,
    CVD_risk_Questionnaire,
    CVD_ModelFeatureMappings
)

# ------------------------------------------------------------------
# 1️⃣ Get HMH model
# ------------------------------------------------------------------

socio_model = ML_Models.objects.get(
    model_name="MRMR_COX_Sociodemographics"
)

# ------------------------------------------------------------------
# 2️⃣ FULL Feature → Question Mapping Table
# ------------------------------------------------------------------

mapping_table = [
("category_Sociodemographics_ts_Age.completed.full.time.education...Instance.0_Lower.third",
 "At what age did you complete your continuous full-time education? Enter age in years. If you never attended school, enter -2."),
("category_Sociodemographics_ts_Age.completed.full.time.education...Instance.0_Middle.third",
 "At what age did you complete your continuous full-time education? Enter age in years. If you never attended school, enter -2."),
("category_Sociodemographics_ts_Age.completed.full.time.education...Instance.0_neg2",
 "At what age did you complete your continuous full-time education? Enter age in years. If you never attended school, enter -2."),
("category_Sociodemographics_ts_Age.completed.full.time.education...Instance.0_Upper.third",
 "At what age did you complete your continuous full-time education? Enter age in years. If you never attended school, enter -2."),

("category_Sociodemographics_ts_Attendance.disability.mobility.allowance...Instance.0_1",
 "Do you receive any of the following? (You can select more than one answer)"),
("category_Sociodemographics_ts_Attendance.disability.mobility.allowance...Instance.0_2",
 "Do you receive any of the following? (You can select more than one answer)"),
("category_Sociodemographics_ts_Attendance.disability.mobility.allowance...Instance.0_3",
 "Do you receive any of the following? (You can select more than one answer)"),
("category_Sociodemographics_ts_Attendance.disability.mobility.allowance...Instance.0_neg7",
 "Do you receive any of the following? (You can select more than one answer)"),

("category_Sociodemographics_ts_Average.total.household.income.before.tax...Instance.0_1",
 "What is the average total income before tax received by your HOUSEHOLD?"),
("category_Sociodemographics_ts_Average.total.household.income.before.tax...Instance.0_2",
 "What is the average total income before tax received by your HOUSEHOLD?"),
("category_Sociodemographics_ts_Average.total.household.income.before.tax...Instance.0_3",
 "What is the average total income before tax received by your HOUSEHOLD?"),
("category_Sociodemographics_ts_Average.total.household.income.before.tax...Instance.0_4",
 "What is the average total income before tax received by your HOUSEHOLD?"),
("category_Sociodemographics_ts_Average.total.household.income.before.tax...Instance.0_5",
 "What is the average total income before tax received by your HOUSEHOLD?"),

("category_Sociodemographics_ts_Current.employment.status...Instance.0_1",
 "Which of the following describes your current situation? (You can select more than one answer)"),
("category_Sociodemographics_ts_Current.employment.status...Instance.0_2",
 "Which of the following describes your current situation? (You can select more than one answer)"),
("category_Sociodemographics_ts_Current.employment.status...Instance.0_3",
 "Which of the following describes your current situation? (You can select more than one answer)"),
("category_Sociodemographics_ts_Current.employment.status...Instance.0_4",
 "Which of the following describes your current situation? (You can select more than one answer)"),
("category_Sociodemographics_ts_Current.employment.status...Instance.0_7",
 "Which of the following describes your current situation? (You can select more than one answer)"),
("category_Sociodemographics_ts_Current.employment.status...Instance.0_neg7",
 "Which of the following describes your current situation? (You can select more than one answer)"),

("category_Sociodemographics_ts_Distance.between.home.and.job.workplace...Instance.0_Lower.third",
 "About how many miles is it between your home and your work?"),
("category_Sociodemographics_ts_Distance.between.home.and.job.workplace...Instance.0_Middle.third",
 "About how many miles is it between your home and your work?"),
("category_Sociodemographics_ts_Distance.between.home.and.job.workplace...Instance.0_Upper.third",
 "About how many miles is it between your home and your work?"),

("category_Sociodemographics_ts_Ethnic.background...Instance.0_1",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_1002",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_1003",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_2002",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_2003",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_3001",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_3002",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_4001",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_4002",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_4003",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_5",
 "What is your ethnic group?"),
("category_Sociodemographics_ts_Ethnic.background...Instance.0_6",
 "What is your ethnic group?"),

("category_Sociodemographics_ts_Length.of.time.at.current.address...Instance.0",
 "How many years have you lived at your current address?"),

("category_Sociodemographics_ts_Number.in.household...Instance.0_Lower.third",
 "Including yourself, how many people are living together in your household? (Include those who usually live in the house such as students living away from home during term, partners in the armed forces or professions such as pilots)"),
("category_Sociodemographics_ts_Number.in.household...Instance.0_Middle.third",
 "Including yourself, how many people are living together in your household? (Include those who usually live in the house such as students living away from home during term, partners in the armed forces or professions such as pilots)"),
("category_Sociodemographics_ts_Number.in.household...Instance.0_Upper.third",
 "Including yourself, how many people are living together in your household? (Include those who usually live in the house such as students living away from home during term, partners in the armed forces or professions such as pilots)"),

("category_Sociodemographics_ts_Own.or.rent.accommodation.lived.in...Instance.0_1",
 "Do you own or rent the accommodation that you live in?"),
("category_Sociodemographics_ts_Own.or.rent.accommodation.lived.in...Instance.0_2",
 "Do you own or rent the accommodation that you live in?"),
("category_Sociodemographics_ts_Own.or.rent.accommodation.lived.in...Instance.0_3",
 "Do you own or rent the accommodation that you live in?"),
("category_Sociodemographics_ts_Own.or.rent.accommodation.lived.in...Instance.0_5",
 "Do you own or rent the accommodation that you live in?"),

("category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_1",
 "What type of accommodation do you live in?"),
("category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_2",
 "What type of accommodation do you live in?"),
("category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_3",
 "What type of accommodation do you live in?"),
("category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_4",
 "What type of accommodation do you live in?"),
("category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_5",
 "What type of accommodation do you live in?"),
("category_Sociodemographics_ts_Type.of.accommodation.lived.in...Instance.0_neg7",
 "What type of accommodation do you live in?"),
# Glasses
("category_Health and medical history_ts_Wears.glasses.or.contact.lenses...Instance.0_1",
 "Do you wear glasses or contact lenses to correct your vision?"),
("category_Health and medical history_ts_Wears.glasses.or.contact.lenses...Instance.0_0",
 "Do you wear glasses or contact lenses to correct your vision?"),
("category_Sociodemographics_ts_Frequency.of.travelling.from.home.to.job.workplace...Instance.0_Lower.third",
 "How many times a WEEK do you travel from home to your main work? (count outward journeys only; put 0 if you always work from home)"),
("category_Sociodemographics_ts_Frequency.of.travelling.from.home.to.job.workplace...Instance.0_Middle.third",
 "How many times a WEEK do you travel from home to your main work? (count outward journeys only; put 0 if you always work from home)"),

("category_Sociodemographics_ts_Gas.or.solid.fuel.cooking.heating...Instance.0_1",
 "Do you have any of the following in your home? (You can select more than one answer)"),
("category_Sociodemographics_ts_Gas.or.solid.fuel.cooking.heating...Instance.0_2",
 "Do you have any of the following in your home? (You can select more than one answer)"),
("category_Sociodemographics_ts_Gas.or.solid.fuel.cooking.heating...Instance.0_3",
 "Do you have any of the following in your home? (You can select more than one answer)"),
("category_Sociodemographics_ts_Gas.or.solid.fuel.cooking.heating...Instance.0_neg7",
 "Do you have any of the following in your home? (You can select more than one answer)"),

("category_Sociodemographics_ts_How.are.people.in.household.related.to.participant...Instance.0_1",
 "How are the other people who live with you related to you? (You can select more than one answer)"),
("category_Sociodemographics_ts_How.are.people.in.household.related.to.participant...Instance.0_2",
 "How are the other people who live with you related to you? (You can select more than one answer)"),
("category_Sociodemographics_ts_How.are.people.in.household.related.to.participant...Instance.0_4",
 "How are the other people who live with you related to you? (You can select more than one answer)"),
("category_Sociodemographics_ts_How.are.people.in.household.related.to.participant...Instance.0_5",
 "How are the other people who live with you related to you? (You can select more than one answer)"),
("category_Sociodemographics_ts_How.are.people.in.household.related.to.participant...Instance.0_6",
 "How are the other people who live with you related to you? (You can select more than one answer)"),
("category_Sociodemographics_ts_How.are.people.in.household.related.to.participant...Instance.0_8",
 "How are the other people who live with you related to you? (You can select more than one answer)"),

("category_Sociodemographics_ts_Job.involves.heavy.manual.or.physical.work...Instance.0_1",
 "Does your work involve heavy manual or physical work?"),
("category_Sociodemographics_ts_Job.involves.heavy.manual.or.physical.work...Instance.0_2",
 "Does your work involve heavy manual or physical work?"),

("category_Sociodemographics_ts_Job.involves.mainly.walking.or.standing...Instance.0_1",
 "Does your work involve walking or standing for most of the time?"),
("category_Sociodemographics_ts_Job.involves.mainly.walking.or.standing...Instance.0_2",
 "Does your work involve walking or standing for most of the time?"),
("category_Sociodemographics_ts_Job.involves.mainly.walking.or.standing...Instance.0_4",
 "Does your work involve walking or standing for most of the time?"),

("category_Sociodemographics_ts_Job.involves.night.shift.work...Instance.0_1",
 "Does your work involve night shifts?"),
("category_Sociodemographics_ts_Job.involves.night.shift.work...Instance.0_2",
 "Does your work involve night shifts?"),
("category_Sociodemographics_ts_Job.involves.night.shift.work...Instance.0_3",
 "Does your work involve night shifts?"),

("category_Sociodemographics_ts_Job.involves.shift.work...Instance.0_1",
 "Does your work involve shift work?"),
("category_Sociodemographics_ts_Job.involves.shift.work...Instance.0_2",
 "Does your work involve shift work?"),
("category_Sociodemographics_ts_Job.involves.shift.work...Instance.0_3",
 "Does your work involve shift work?"),
("category_Sociodemographics_ts_Job.involves.shift.work...Instance.0_4",
 "Does your work involve shift work?"),

("category_Sociodemographics_ts_Length.of.working.week.for.main.job...Instance.0_Lower.third",
 "In a typical WEEK, how many hours do you spend at work?(Do not include hours travelling to and from work)"),
("category_Sociodemographics_ts_Length.of.working.week.for.main.job...Instance.0_Middle.third",
 "In a typical WEEK, how many hours do you spend at work?(Do not include hours travelling to and from work)"),
("category_Sociodemographics_ts_Length.of.working.week.for.main.job...Instance.0_Upper.third",
 "In a typical WEEK, how many hours do you spend at work?(Do not include hours travelling to and from work)"),

("category_Sociodemographics_ts_Number.of.vehicles.in.household...Instance.0_1",
 "How many cars or vans are owned, or available for use, by you or members of your household? (Please include company vehicles if available for private use)"),
("category_Sociodemographics_ts_Number.of.vehicles.in.household...Instance.0_2",
 "How many cars or vans are owned, or available for use, by you or members of your household? (Please include company vehicles if available for private use)"),
("category_Sociodemographics_ts_Number.of.vehicles.in.household...Instance.0_3",
 "How many cars or vans are owned, or available for use, by you or members of your household? (Please include company vehicles if available for private use)"),
("category_Sociodemographics_ts_Number.of.vehicles.in.household...Instance.0_4",
 "How many cars or vans are owned, or available for use, by you or members of your household? (Please include company vehicles if available for private use)"),
("category_Sociodemographics_ts_Number.of.vehicles.in.household...Instance.0_5",
 "How many cars or vans are owned, or available for use, by you or members of your household? (Please include company vehicles if available for private use)"),
# Age started glasses
("category_Health and medical history_ts_Age.started.wearing.glasses.or.contact.lenses...Instance.0_Lower.third",
 "What age did you first start to wear glasses or contact lenses?"),
("category_Health and medical history_ts_Age.started.wearing.glasses.or.contact.lenses...Instance.0_Middle.third",
 "What age did you first start to wear glasses or contact lenses?"),
("category_Health and medical history_ts_Age.started.wearing.glasses.or.contact.lenses...Instance.0_Upper.third",
 "What age did you first start to wear glasses or contact lenses?"),
 ("category_Sociodemographics_ts_Qualifications...Instance.0_1",
 "Which of the following qualifications do you have?\n(You can select more than one)"),
("category_Sociodemographics_ts_Qualifications...Instance.0_2",
 "Which of the following qualifications do you have?\n(You can select more than one)"),
("category_Sociodemographics_ts_Qualifications...Instance.0_3",
 "Which of the following qualifications do you have?\n(You can select more than one)"),
("category_Sociodemographics_ts_Qualifications...Instance.0_4",
 "Which of the following qualifications do you have?\n(You can select more than one)"),
("category_Sociodemographics_ts_Qualifications...Instance.0_6",
 "Which of the following qualifications do you have?\n(You can select more than one)"),
("category_Sociodemographics_ts_Qualifications...Instance.0_neg7",
 "Which of the following qualifications do you have?\n(You can select more than one)"),

("category_Sociodemographics_ts_Time.employed.in.main.current.job...Instance.0_Lower.third",
 "How many years have you worked in your current job? (If you have more than one job please answer this, and the following questions on work, for your MAIN job only)"),
("category_Sociodemographics_ts_Time.employed.in.main.current.job...Instance.0_Middle.third",
 "How many years have you worked in your current job? (If you have more than one job please answer this, and the following questions on work, for your MAIN job only)"),
("category_Sociodemographics_ts_Time.employed.in.main.current.job...Instance.0_Upper.third",
 "How many years have you worked in your current job? (If you have more than one job please answer this, and the following questions on work, for your MAIN job only)"),

("category_Sociodemographics_ts_Transport.type.for.commuting.to.job.workplace...Instance.0_1",
 "What types of transport do you use to get to and from work? (You can select more than one answer)"),
("category_Sociodemographics_ts_Transport.type.for.commuting.to.job.workplace...Instance.0_2",
 "What types of transport do you use to get to and from work? (You can select more than one answer)"),
("category_Sociodemographics_ts_Transport.type.for.commuting.to.job.workplace...Instance.0_3",
 "What types of transport do you use to get to and from work? (You can select more than one answer)"),
("category_Sociodemographics_ts_Transport.type.for.commuting.to.job.workplace...Instance.0_4",
 "What types of transport do you use to get to and from work? (You can select more than one answer)"),
("category_Sociodemographics_ts_Transport.type.for.commuting.to.job.workplace...Instance.0_neg7",
 "What types of transport do you use to get to and from work? (You can select more than one answer)"),

("category_Sociodemographics_ts_Year.immigrated.to.UK..United.Kingdom....Instance.0_Upper.third",
 "What year did you first come to live in the United Kingdom?"),

 ("Age.at.recruitment",
 "What is your age in years at the time of this test? "),

]

# ------------------------------------------------------------------
# 3️⃣ Create / Fix Features + Map To Model
# ------------------------------------------------------------------

for feature_name, question_text in mapping_table:

    try:
        question = CVD_risk_Questionnaire.objects.filter(
            question_text__icontains=question_text[:30]
        ).first()

        if not question:
            raise Exception(f"❌ Question not found: {repr(question_text)}")
    except CVD_risk_Questionnaire.DoesNotExist:
        print("❌ FAILED ON QUESTION:")
        print(repr(question_text))
        raise

    feature, created = CVD_Risk_Model_InputFeatures.objects.get_or_create(
        feature_name=feature_name,
        defaults={"question": question}
    )

    if not created and feature.question != question:
        feature.question = question
        feature.save()

    CVD_ModelFeatureMappings.objects.get_or_create(
        model=socio_model,
        input_feature=feature
    )

    print("Processed:", feature_name)

print("Socio mapping complete.")