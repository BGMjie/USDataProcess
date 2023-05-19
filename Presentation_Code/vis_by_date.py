import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
biden = pd.read_csv('/Users/zhaoyi/PycharmProjects/pythonProject/Biden_final.csv', index_col=0)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

def count_date(date1, date2):
    biden['Dates'] = pd.to_datetime(biden['Dates'])
    filtered_visits = biden[(biden['Dates'] >= date1) & (biden['Dates'] <= date2)]
    x = filtered_visits.copy()
    x.loc[:, 'Countries_inv'] = x.loc[:, 'Countries_inv'].str.split(';;')
    x_expanded = x.explode('Countries_inv')
    country_count = x_expanded['Countries_inv'].value_counts()
    date_df = pd.DataFrame({'Country': country_count.index, 'Count': country_count.values})
    merged_date = world.merge(date_df, left_on='name', right_on='Country')
    merged_date.plot(column='Count', cmap='Greens', legend=True, scheme='quantiles', edgecolor='black', linewidth=0.5,
                     figsize=(15, 10))
    return date_df

count_date('2017-05-01', '2017-07-31')
plt.show()

