import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
biden = pd.read_csv('/Users/zhaoyi/PycharmProjects/pythonProject/Biden_final.csv', index_col=0)
meeting = pd.read_csv('/Users/zhaoyi/PycharmProjects/pythonProject/Biden_Meetings.csv', index_col=0)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

def count_visit(df):
    df['Countries_inv'] = df['Countries_inv'].str.split(';;')
    df_expand = df.explode('Countries_inv')
    visit = df_expand['Countries_inv'].value_counts()
    visit_df = pd.DataFrame({'Country': visit.index, 'Count': visit.values})
    return visit_df

def count_meet(df):
    df['Count_inv'] = df['Count_inv'].str.split(';;')
    df_expand = df.explode('Count_inv')
    meet = df_expand['Count_inv'].value_counts()
    meet_df = pd.DataFrame({'Country': meet.index, 'Count': meet.values})
    return meet_df

def plot_count(type1, type2):
    type1 = count_visit(type1)
    type2 = count_meet(type2)
    merged_visit = world.merge(type1, left_on='name', right_on='Country')
    merged_meet = world.merge(type2, left_on='name', right_on='Country')
    merged_visit.plot(column='Count', cmap='Blues', legend=True, scheme='quantiles', edgecolor='black', linewidth=0.5,
                figsize=(15, 10))
    merged_meet.plot(column='Count', cmap='Reds', legend=True, scheme='quantiles', edgecolor='black', linewidth=0.5,
                figsize=(15, 10))
    return merged_visit, merged_meet

plot_count(biden, meeting)
plt.show()