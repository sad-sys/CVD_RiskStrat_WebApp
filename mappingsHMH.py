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

hmh_model = ML_Models.objects.get(
    model_name="MRMR_COX_Sociodemographics_Health_and_medical_history"
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

# Mouth / dental
("category_Health and medical history_ts_Mouth.teeth.dental.problems...Instance.0_2",
 "Do you have any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mouth.teeth.dental.problems...Instance.0_3",
 "Do you have any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mouth.teeth.dental.problems...Instance.0_4",
 "Do you have any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mouth.teeth.dental.problems...Instance.0_5",
 "Do you have any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mouth.teeth.dental.problems...Instance.0_6",
 "Do you have any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mouth.teeth.dental.problems...Instance.0_neg7",
 "Do you have any of the following? (You can select more than one answer)"),

# Overall health
("category_Health and medical history_ts_Overall.health.rating...Instance.0_1",
 "In general how would you rate your overall health?"),
("category_Health and medical history_ts_Overall.health.rating...Instance.0_2",
 "In general how would you rate your overall health?"),
("category_Health and medical history_ts_Overall.health.rating...Instance.0_3",
 "In general how would you rate your overall health?"),
("category_Health and medical history_ts_Overall.health.rating...Instance.0_4",
 "In general how would you rate your overall health?"),

# Long-standing illness
("category_Health and medical history_ts_Long.standing.illness..disability.or.infirmity...Instance.0_0",
 "Do you have any long-standing illness, disability or infirmity?"),
("category_Health and medical history_ts_Long.standing.illness..disability.or.infirmity...Instance.0_1",
 "Do you have any long-standing illness, disability or infirmity?"),

# Falls
("category_Health and medical history_ts_Falls.in.the.last.year...Instance.0_1",
 "In the last year have you had any falls?"),
("category_Health and medical history_ts_Falls.in.the.last.year...Instance.0_2",
 "In the last year have you had any falls?"),
("category_Health and medical history_ts_Falls.in.the.last.year...Instance.0_3",
 "In the last year have you had any falls?"),

# Weight change
("category_Health and medical history_ts_Weight.change.compared.with.1.year.ago...Instance.0_0",
 "Compared with one year ago, has your weight changed?"),
("category_Health and medical history_ts_Weight.change.compared.with.1.year.ago...Instance.0_3",
 "Compared with one year ago, has your weight changed?"),

# Wheeze
("category_Health and medical history_ts_Wheeze.or.whistling.in.the.chest.in.last.year...Instance.0_0",
 "In the last year have you ever had wheeze or whistling in the chest?"),
("category_Health and medical history_ts_Wheeze.or.whistling.in.the.chest.in.last.year...Instance.0_1",
 "In the last year have you ever had wheeze or whistling in the chest?"),

# Chest pain
("category_Health and medical history_ts_Chest.pain.or.discomfort...Instance.0_0",
 "Do you ever have any pain or discomfort in your chest?"),
("category_Health and medical history_ts_Chest.pain.or.discomfort...Instance.0_1",
 "Do you ever have any pain or discomfort in your chest?"),

("category_Health and medical history_ts_Chest.pain.or.discomfort.walking.normally...Instance.0_0",
 "Do you get this pain or discomfort when you walk at an ordinary pace on the level?"),
("category_Health and medical history_ts_Chest.pain.or.discomfort.walking.normally...Instance.0_1",
 "Do you get this pain or discomfort when you walk at an ordinary pace on the level?"),

("category_Health and medical history_ts_Chest.pain.or.discomfort.when.walking.uphill.or.hurrying...Instance.0_0",
 "Do you get this pain or discomfort when you walk uphill or hurry?"),
("category_Health and medical history_ts_Chest.pain.or.discomfort.when.walking.uphill.or.hurrying...Instance.0_1",
 "Do you get this pain or discomfort when you walk uphill or hurry?"),

("category_Health and medical history_ts_Chest.pain.due.to.walking.ceases.when.standing.still...Instance.0_0",
 "Does this chest pain go away when you stand still?"),
("category_Health and medical history_ts_Chest.pain.due.to.walking.ceases.when.standing.still...Instance.0_1",
 "Does this chest pain go away when you stand still?"),

# Diabetes
("category_Health and medical history_ts_Diabetes.diagnosed.by.doctor...Instance.0_0",
 "Has a doctor ever told you that you have diabetes?"),
("category_Health and medical history_ts_Diabetes.diagnosed.by.doctor...Instance.0_1",
 "Has a doctor ever told you that you have diabetes?"),

# Cancer
("category_Health and medical history_ts_Cancer.diagnosed.by.doctor...Instance.0_0",
 "Has a doctor ever told you that you have had cancer?"),
("category_Health and medical history_ts_Cancer.diagnosed.by.doctor...Instance.0_1",
 "Has a doctor ever told you that you have had cancer?"),

# Hearing
("category_Health and medical history_ts_Hearing.difficulty.problems...Instance.0_0",
 "Do you have any difficulty with your hearing?"),
("category_Health and medical history_ts_Hearing.difficulty.problems...Instance.0_1",
 "Do you have any difficulty with your hearing?"),

("category_Health and medical history_ts_Hearing.difficulty.problems.with.background.noise...Instance.0_0",
 "Do you find it difficult to follow a conversation if there is background noise (such as TV, radio, children playing)?"),
("category_Health and medical history_ts_Hearing.difficulty.problems.with.background.noise...Instance.0_1",
 "Do you find it difficult to follow a conversation if there is background noise (such as TV, radio, children playing)?"),

("category_Health and medical history_ts_Hearing.aid.user...Instance.0_0",
 "Do you use a hearing aid most of the time?"),
("category_Health and medical history_ts_Hearing.aid.user...Instance.0_1",
 "Do you use a hearing aid most of the time?"),

# Pain types last month
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_1",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_3",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_4",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_5",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_6",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_7",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_8",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),
("category_Health and medical history_ts_Pain.type.s..experienced.in.last.month...Instance.0_neg7",
 "In the last month have you experienced any of the following that interfered with your usual activities?\n(You can select more than one answer)"),

 ("category_Health and medical history_ts_Headaches.for.3..months...Instance.0_0",
 "Have you had headaches for more than 3 months?"),
("category_Health and medical history_ts_Facial.pains.for.3..months...Instance.0_1",
 "Have you had facial pains for more than 3 months?"),
("category_Health and medical history_ts_Neck.shoulder.pain.for.3..months...Instance.0_1",
 "Have you had neck or shoulder pains for more than 3 months?"),
("category_Health and medical history_ts_Back.pain.for.3..months...Instance.0_1",
 "Have you had back pains for more than 3 months?"),
("category_Health and medical history_ts_Stomach.abdominal.pain.for.3..months...Instance.0_1",
 "Have you had stomach or abdominal pains for more than 3 months?"),
("category_Health and medical history_ts_Hip.pain.for.3..months...Instance.0_1",
 "Have you had hip pains for more than 3 months?"),
("category_Health and medical history_ts_Hip.pain.for.3..months...Instance.0_0",
 "Have you had hip pains for more than 3 months?"),
("category_Health and medical history_ts_Knee.pain.for.3..months...Instance.0_1",
 "Have you had knee pains for more than 3 months?"),
("category_Health and medical history_ts_General.pain.for.3..months...Instance.0_1",
 "Have you had pains all over the body for more than 3 months?"),
("category_Health and medical history_ts_General.pain.for.3..months...Instance.0_0",
 "Have you had pains all over the body for more than 3 months?"),

 ("category_Health and medical history_ts_Ever.had.bowel.cancer.screening...Instance.0_0",
 "Have you ever had a screening test for bowel (colorectal) cancer?\n(Please include tests for blood in the stool/faeces or a colonoscopy or a sigmoidoscopy)"),
("category_Health and medical history_ts_Ever.had.bowel.cancer.screening...Instance.0_1",
 "Have you ever had a screening test for bowel (colorectal) cancer?\n(Please include tests for blood in the stool/faeces or a colonoscopy or a sigmoidoscopy)"),
("category_Health and medical history_ts_Most.recent.bowel.cancer.screening...Instance.0_Lower.third",
 "How many years ago was the most recent one of these tests?"),
("category_Health and medical history_ts_Most.recent.bowel.cancer.screening...Instance.0_Middle.third",
 "How many years ago was the most recent one of these tests?"),
("category_Health and medical history_ts_Most.recent.bowel.cancer.screening...Instance.0_Upper.third",
 "How many years ago was the most recent one of these tests?"),

 ("category_Health and medical history_ts_Time.since.last.prostate.specific.antigen..PSA..test...Instance.0_Lower.third",
 "How many years ago was your last test?"),
("category_Health and medical history_ts_Time.since.last.prostate.specific.antigen..PSA..test...Instance.0_Middle.third",
 "How many years ago was your last test?"),
("category_Health and medical history_ts_Time.since.last.prostate.specific.antigen..PSA..test...Instance.0_Upper.third",
 "How many years ago was your last test?"),

("category_Health and medical history_ts_Gestational.diabetes.only...Instance.0_0",
 "Did you only have diabetes during pregnancy?"),
("category_Health and medical history_ts_Gestational.diabetes.only...Instance.0_neg2",
 "Did you only have diabetes during pregnancy?"),
("category_Health and medical history_ts_Age.diabetes.diagnosed...Instance.0_Lower.third",
 "What was your age when the diabetes was first diagnosed?"),
("category_Health and medical history_ts_Age.diabetes.diagnosed...Instance.0_Middle.third",
 "What was your age when the diabetes was first diagnosed?"),
("category_Health and medical history_ts_Age.diabetes.diagnosed...Instance.0_Upper.third",
 "What was your age when the diabetes was first diagnosed?"),
("category_Health and medical history_ts_Started.insulin.within.one.year.diagnosis.of.diabetes...Instance.0_0",
 "Did you start insulin within one year of your diagnosis of diabetes?"),
("category_Health and medical history_ts_Started.insulin.within.one.year.diagnosis.of.diabetes...Instance.0_1",
 "Did you start insulin within one year of your diagnosis of diabetes?"),

 ("category_Health and medical history_ts_Fractured.broken.bones.in.last.5.years...Instance.0_0",
 "Have you fractured/broken any bones in the last 5 years?"),
("category_Health and medical history_ts_Fractured.broken.bones.in.last.5.years...Instance.0_1",
 "Have you fractured/broken any bones in the last 5 years?"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_1",
 "Which bones did you fracture/break? (You can select more than one answer)"),
# add all 2–7 variants same question

("category_Health and medical history_ts_Fracture.resulting.from.simple.fall...Instance.0_1",
 "Did the fracture result from a simple fall (i.e. from standing height)?"),
 ("category_Health and medical history_ts_Vascular.heart.problems.diagnosed.by.doctor...Instance.0_1",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),
("category_Health and medical history_ts_Vascular.heart.problems.diagnosed.by.doctor...Instance.0_2",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),
("category_Health and medical history_ts_Vascular.heart.problems.diagnosed.by.doctor...Instance.0_3",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),
("category_Health and medical history_ts_Vascular.heart.problems.diagnosed.by.doctor...Instance.0_4",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),
("category_Health and medical history_ts_Vascular.heart.problems.diagnosed.by.doctor...Instance.0_neg7",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),
 ("category_Health and medical history_ts_Age.heart.attack.diagnosed...Instance.0_Lower.third",
 "What was your age when the heart attack was first diagnosed?"),
("category_Health and medical history_ts_Age.heart.attack.diagnosed...Instance.0_Upper.third",
 "What was your age when the heart attack was first diagnosed?"),
 ("category_Health and medical history_ts_Age.angina.diagnosed...Instance.0_Lower.third",
 "What was your age when the angina was first diagnosed?"),
("category_Health and medical history_ts_Age.angina.diagnosed...Instance.0_Upper.third",
 "What was your age when the angina was first diagnosed?"),
 ("category_Health and medical history_ts_Age.stroke.diagnosed...Instance.0_Lower.third",
 "What was your age when the stroke was first diagnosed?"),
("category_Health and medical history_ts_Age.stroke.diagnosed...Instance.0_Upper.third",
 "What was your age when the stroke was first diagnosed?"),
 ("category_Health and medical history_ts_Age.high.blood.pressure.diagnosed...Instance.0_Lower.third",
 "What was your age when the high blood pressure was first diagnosed?"),
("category_Health and medical history_ts_Age.high.blood.pressure.diagnosed...Instance.0_Upper.third",
 "What was your age when the high blood pressure was first diagnosed?"),
 ("category_Health and medical history_ts_Age.deep.vein.thrombosis..DVT..blood.clot.in.leg..diagnosed...Instance.0_Lower.third",
 "What was your age when the blood clot in the leg (DVT) was first diagnosed?"),
("category_Health and medical history_ts_Age.deep.vein.thrombosis..DVT..blood.clot.in.leg..diagnosed...Instance.0_Upper.third",
 "What was your age when the blood clot in the leg (DVT) was first diagnosed?"),
 ("category_Health and medical history_ts_Age.pulmonary.embolism..blood.clot.in.lung..diagnosed...Instance.0_Lower.third",
 "What was your age when the blood clot in the lung was first diagnosed?"),
("category_Health and medical history_ts_Age.pulmonary.embolism..blood.clot.in.lung..diagnosed...Instance.0_Upper.third",
 "What was your age when the blood clot in the lung was first diagnosed?"),
 ("category_Health and medical history_ts_Age.emphysema.chronic.bronchitis.diagnosed...Instance.0_Lower.third",
 "What was your age when the emphysema/chronic bronchitis was first diagnosed?"),
("category_Health and medical history_ts_Age.emphysema.chronic.bronchitis.diagnosed...Instance.0_Upper.third",
 "What was your age when the emphysema/chronic bronchitis was first diagnosed?"),
 ("category_Health and medical history_ts_Age.asthma.diagnosed...Instance.0_Lower.third",
 "What was your age when the asthma was first diagnosed?"),
("category_Health and medical history_ts_Age.asthma.diagnosed...Instance.0_Upper.third",
 "What was your age when the asthma was first diagnosed?"),
 ("category_Health and medical history_ts_Age.hay.fever..rhinitis.or.eczema.diagnosed...Instance.0_Lower.third",
 "What was your age when the hayfever, rhinitis or eczema was first diagnosed?"),
("category_Health and medical history_ts_Age.hay.fever..rhinitis.or.eczema.diagnosed...Instance.0_Upper.third",
 "What was your age when the hayfever, rhinitis or eczema was first diagnosed?"),
 ("category_Health and medical history_ts_Age.diabetes.diagnosed...Instance.0_Lower.third",
 "What was your age when the diabetes was first diagnosed?"),
("category_Health and medical history_ts_Age.diabetes.diagnosed...Instance.0_Upper.third",
 "What was your age when the diabetes was first diagnosed?"),
 ("category_Health and medical history_ts_Time.since.last.prostate.specific.antigen..PSA..test...Instance.0_Lower.third",
 "How many years ago was your last test?"),
("category_Health and medical history_ts_Time.since.last.prostate.specific.antigen..PSA..test...Instance.0_Upper.third",
 "How many years ago was your last test?"),

 ("category_Health and medical history_ts_Other.serious.medical.condition.disability.diagnosed.by.doctor...Instance.0_0",
 "Has a doctor ever told you that you have any other serious medical condition or disability?"),
("category_Health and medical history_ts_Other.serious.medical.condition.disability.diagnosed.by.doctor...Instance.0_1",
 "Has a doctor ever told you that you have any other serious medical condition or disability?"),

("category_Health and medical history_ts_Medication.for.pain.relief..constipation..heartburn...Instance.0_1",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Medication.for.pain.relief..constipation..heartburn...Instance.0_3",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Medication.for.pain.relief..constipation..heartburn...Instance.0_4",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Medication.for.pain.relief..constipation..heartburn...Instance.0_5",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Medication.for.pain.relief..constipation..heartburn...Instance.0_6",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Medication.for.pain.relief..constipation..heartburn...Instance.0_neg7",
 "Do you regularly take any of the following? (You can select more than one answer)"),

("category_Health and medical history_ts_Mineral.and.other.dietary.supplements...Instance.0_1",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mineral.and.other.dietary.supplements...Instance.0_3",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mineral.and.other.dietary.supplements...Instance.0_4",
 "Do you regularly take any of the following? (You can select more than one answer)"),
("category_Health and medical history_ts_Mineral.and.other.dietary.supplements...Instance.0_5",
 "Do you regularly take any of the following? (You can select more than one answer)"),
 ("category_Health and medical history_ts_Mineral.and.other.dietary.supplements...Instance.0_neg7",
 "Do you regularly take any of the following? (You can select more than one answer)"),


("category_Health and medical history_ts_Combined.sex.medication_1",
 "Do you regularly take any of the following medications? (you can select more than one answer)"),
("category_Health and medical history_ts_Combined.sex.medication_2",
 "Do you regularly take any of the following medications? (you can select more than one answer)"),
("category_Health and medical history_ts_Combined.sex.medication_3",
 "Do you regularly take any of the following medications? (you can select more than one answer)"),
("category_Health and medical history_ts_Combined.sex.medication_4",
 "Do you regularly take any of the following medications? (you can select more than one answer)"),
("category_Health and medical history_ts_Combined.sex.medication_5",
 "Do you regularly take any of the following medications? (you can select more than one answer)"),


 ("category_Health and medical history_ts_Taking.other.prescription.medications...Instance.0_0",
 "Do you regularly take any other PRESCRIPTION medications? (Do not forget medications such as puffers or patches)"),
("category_Health and medical history_ts_Taking.other.prescription.medications...Instance.0_1",
 "Do you regularly take any other PRESCRIPTION medications? (Do not forget medications such as puffers or patches)"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_2",
 "Which bones did you fracture/break? (You can select more than one answer)"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_3",
 "Which bones did you fracture/break? (You can select more than one answer)"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_4",
 "Which bones did you fracture/break? (You can select more than one answer)"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_5",
 "Which bones did you fracture/break? (You can select more than one answer)"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_6",
 "Which bones did you fracture/break? (You can select more than one answer)"),

("category_Health and medical history_ts_Fractured.bone.site.s....Instance.0_7",
 "Which bones did you fracture/break? (You can select more than one answer)"),

 ("category_Health and medical history_ts_Combined.sex.major.operations_0",
 "Have you had any major operations? (For example, operations that required an overnight stay in hospital)"),

("category_Health and medical history_ts_Combined.sex.major.operations_1",
 "Have you had any major operations? (For example, operations that required an overnight stay in hospital)"),
 ("category_Health and medical history_ts_Blood.clot..DVT..bronchitis..emphysema..asthma..rhinitis..eczema..allergy.diagnosed.by.doctor...Instance.0_5",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),

("category_Health and medical history_ts_Blood.clot..DVT..bronchitis..emphysema..asthma..rhinitis..eczema..allergy.diagnosed.by.doctor...Instance.0_6",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),

("category_Health and medical history_ts_Blood.clot..DVT..bronchitis..emphysema..asthma..rhinitis..eczema..allergy.diagnosed.by.doctor...Instance.0_7",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),

("category_Health and medical history_ts_Blood.clot..DVT..bronchitis..emphysema..asthma..rhinitis..eczema..allergy.diagnosed.by.doctor...Instance.0_8",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),

("category_Health and medical history_ts_Blood.clot..DVT..bronchitis..emphysema..asthma..rhinitis..eczema..allergy.diagnosed.by.doctor...Instance.0_9",
 "Has a doctor ever told you that you have had any of the following conditions? (You can select more than one answer)"),




 ("clinicalrisk_Age.at.recruitment",
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
        model=hmh_model,
        input_feature=feature
    )

    print("Processed:", feature_name)

print("HMH mapping complete.")