import pandas as pd


file_path = 'survey_results_public.csv'
file_path2 = 'survey_results_schema.csv'
df = pd.read_csv(file_path)
schema1 = pd.read_csv(file_path2)


#Кількість респондентів які пройшли опитування
count_userId=df['ResponseId'].count()
print(f"Число юзерів хто пройшов опитування: {count_userId}")

#2Скільки респондентів відповіли на всі запитання?
questions = set(schema1.qname.unique()) & set(df.columns)
complete_answers=df.dropna(subset=questions).shape[0]
print(f"Count respondent who answered all questions: {complete_answers}")


#значення мір центральної тенденції для досвіду (WorkExp) респондентів
df['WorkExp'] = pd.to_numeric(df['WorkExp'], errors='coerce')
work_experience = df['WorkExp'].dropna()
mean_work_experience = work_experience.mean()
median_work_experience = work_experience.median()
mode_work_experience = work_experience.mode()[0] if not work_experience.mode().empty else None
min_work_experience = work_experience.min()
max_work_experience = work_experience.max()
percentile_25 = work_experience.quantile(0.25)
percentile_50 = work_experience.quantile(0.5)
percentile_75 = work_experience.quantile(0.75)
print(print(f"Average: {mean_work_experience}"))
print(print(f"Median: {median_work_experience}"))
print(f"Mode: {mode_work_experience}")
print(f"Min: {min_work_experience}")
print(f"Max: {max_work_experience}")
print(f"25-й percentile: {percentile_25}")
print(f"50-й percentile: {percentile_50}")
print(f"75-й percentile: {percentile_75}")

#Скільки респондентів працює віддалено?
remote_work = df[(df['RemoteWork'] == 'Remote')].shape[0]
print(f"Count users who work remote: {remote_work}")

#Який відсоток респондентів програмує на Python?
python_df = df['LanguageHaveWorkedWith'].str.contains('Python')
python_perc = round(python_df.sum()/count_userId*100)
print(f"users who coded Python: {python_perc} %")

#Скільки респондентів навчалося програмувати за допомогою онлайн курсів?
online_code = df['LearnCode'].str.contains('Online Courses or Certification').sum()
print(f"Count users who studied online {online_code}")

#Серед респондентів що програмують на Python в групуванні по країнам,
#яка середня та медіанна сума компенсації (ConvertedCompYearly) в кожній країні?
python_users_df = df[df['LanguageHaveWorkedWith'].str.contains('Python',na=False)]
grouped_users_country = python_users_df.groupby('Country')
mean_median_ConvertedCompYearly = grouped_users_country['ConvertedCompYearly'].agg(['mean', 'median'])
print(mean_median_ConvertedCompYearly)

#Які рівні освіти мають 5 респондентів з найбільшою компенсацією?
max_ConvertedCompYearly_df = df.nlargest(5, 'ConvertedCompYearly')[['ConvertedCompYearly', 'EdLevel']]
print(max_ConvertedCompYearly_df)

#В кожній віковій категорії, який відсоток респондентів програмує на Python?
df['Python'] = df['LanguageHaveWorkedWith'].str.contains('Python', case=False, na=False)
age_python_counts = df[df['Python']].groupby('Age').size()
age_counts = df['Age'].value_counts()
percentage_python = (age_python_counts / age_counts * 100).fillna(0).round(0)
print(f"Python for ages: {percentage_python} %")

#Серед респондентів що знаходяться в 75 перцентилі за компенсацією середнього і працюють віддалено,
# які індустрії є найрозповсюдженішими?
result = df[(df.ConvertedCompYearly > df.ConvertedCompYearly.quantile(0.75)) &
   (df.RemoteWork == 'Remote')].Industry.value_counts().reset_index()
print(result)