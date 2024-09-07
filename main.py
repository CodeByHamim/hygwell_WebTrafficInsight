import pandas as pd
from scipy.stats import pearsonr, chi2_contingency

file_path = r'C:\Users\hashr\Desktop\hygwell- Assingment2\traffic.csv'
data = pd.read_csv(file_path)

data['date'] = pd.to_datetime(data['date'])

# Filter click and pageview events
click_data = data[data['event'] == 'click']
pageview_data = data[data['event'] == 'pageview']

#Total and Daily Pageview Events:
total_pageviews = pageview_data.shape[0]
average_pageviews_per_day = pageview_data.groupby(pageview_data['date'].dt.date).size().mean()

print(f"Total pageviews: {total_pageviews}")
print(f"Average pageviews per day: {average_pageviews_per_day}")

#Analysis of Other Events:
event_distribution = data['event'].value_counts()
geo_distribution = pageview_data['country'].value_counts()

print(event_distribution)
print(geo_distribution)

# Click-Through Rate (CTR) Analysis:
total_clicks = click_data.shape[0]
overall_ctr = total_clicks / total_pageviews if total_pageviews != 0 else 0
print(f"Overall CTR: {overall_ctr:.4f}")

clicks_by_link = click_data.groupby('linkid').size()
pageviews_by_link = pageview_data.groupby('linkid').size()

ctr_by_link = (clicks_by_link / pageviews_by_link).dropna()
print("\nCTR by Link:")
print(ctr_by_link)

# Correlation Analysis:
correlation_data = pd.DataFrame({'clicks': clicks_by_link, 'pageviews': pageviews_by_link}).fillna(0)

corr_coef, p_value = pearsonr(correlation_data['clicks'], correlation_data['pageviews'])
print(f"\nPearson Correlation: {corr_coef:.4f}, P-value: {p_value:.4f}")

correlation_data['clicks_binary'] = (correlation_data['clicks'] > 0).astype(int)
correlation_data['pageviews_binary'] = (correlation_data['pageviews'] > 0).astype(int)

contingency_table = pd.crosstab(correlation_data['clicks_binary'], correlation_data['pageviews_binary'])
chi2_stat, chi2_p_value, _, _ = chi2_contingency(contingency_table)

print(f"\nChi-Squared Statistic: {chi2_stat:.4f}, P-value: {chi2_p_value:.4f}")
