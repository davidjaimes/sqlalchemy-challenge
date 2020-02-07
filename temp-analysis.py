import pandas as pd
from scipy import stats

measurements = pd.read_csv('data/hawaii_measurements.csv')
measurements['month'] = pd.to_datetime(measurements.date).dt.month
june = measurements[measurements['month'] == 6]
december = measurements[measurements['month'] == 12]
june_grp = june.groupby('station')
december_grp = december.groupby('station')
june_avg = june_grp.tobs.mean()
december_avg = december_grp.tobs.mean()
print(stats.ttest_rel(june_avg, december_avg))
print('''I did a paired t-test because these are temperature observations from the same stations across two different months. The results return a small p-value (p < 0.05) which indicates a statistically significant difference between June and December temperatures across all years.''')
