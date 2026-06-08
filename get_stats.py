import pandas as pd
import numpy as np

df = pd.read_csv('responses.csv')

print('=== DATASET STATISTICS ===')
print(f'Total Responses: {len(df)}')
print(f'\nSatisfaction Distribution:')
print(df['satisfaction'].value_counts().sort_index())
print(f'\nNPS Distribution:')
print(df['nps'].value_counts().sort_index())
print(f'\nCategory Distribution:')
print(df['category'].value_counts())
print(f'\nDelivery Distribution:')
print(df['delivery'].value_counts())

print(f'\n=== CORRELATION ANALYSIS ===')
df['delivery_numeric'] = df['delivery'].map({'Yes': 1, 'No': 0})
corr = df[['satisfaction', 'nps', 'delivery_numeric']].corr()
print('Satisfaction-NPS Correlation: {:.3f}'.format(corr.loc['satisfaction', 'nps']))
print('Satisfaction-Delivery Correlation: {:.3f}'.format(corr.loc['satisfaction', 'delivery_numeric']))
print('NPS-Delivery Correlation: {:.3f}'.format(corr.loc['nps', 'delivery_numeric']))

print(f'\n=== MEAN VALUES ===')
print(f'Average Satisfaction: {df["satisfaction"].mean():.2f}')
print(f'Average NPS: {df["nps"].mean():.2f}')
print(f'On-Time Delivery Rate: {(df["delivery"] == "Yes").sum() / len(df):.1%}')

print(f'\n=== CONDITIONAL PROBABILITIES ===')
high_sat = df[df['satisfaction'] >= 4]
low_sat = df[df['satisfaction'] <= 2]
yes_delivery = df[df['delivery'] == 'Yes']
no_delivery = df[df['delivery'] == 'No']

p1 = len(df[(df["satisfaction"] >= 4) & (df["nps"] >= 8)]) / len(high_sat) if len(high_sat) > 0 else 0
p2 = len(df[(df["satisfaction"] >= 4) & (df["delivery"] == "Yes")]) / len(yes_delivery) if len(yes_delivery) > 0 else 0
p3 = len(df[(df["satisfaction"] >= 4) & (df["delivery"] == "No")]) / len(no_delivery) if len(no_delivery) > 0 else 0

print(f'P(NPS >= 8 | Satisfaction >= 4): {p1:.3f}')
print(f'P(Satisfaction >= 4 | Delivery = Yes): {p2:.3f}')
print(f'P(Satisfaction >= 4 | Delivery = No): {p3:.3f}')

print(f'\n=== TEXT METRICS ===')
unique_feedback = df['feedback'].nunique()
print(f'Unique Feedback Responses: {unique_feedback}')
print(f'Duplicate Feedback Rate: {(len(df) - unique_feedback) / len(df):.2%}')
lengths = df['feedback'].str.split().str.len()
print(f'Average Feedback Length: {lengths.mean():.1f} words')
print(f'Median Feedback Length: {lengths.median():.1f} words')
