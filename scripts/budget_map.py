import json
import os.path as op
import pandas as pd
import folium


if __name__ == "__main__":
    budget_df = pd.read_csv(op.join('..', 'data', 'budget.csv'))
    budget_sum_df = budget_df.groupby(["เขต", "latitude", "longitude"])['งบแผนงาน'].sum().reset_index()
    folium_map = folium.Map(location=[13.738, 100.597],
                            zoom_start=11,
                            tiles="Stamen Toner")

    for _, row in budget_sum_df.iterrows():
        if row['latitude'] != "":
            folium.CircleMarker(location=(row["latitude"],
                                        row["longitude"]),
                                radius=row['งบแผนงาน'] / 50000000,
                                color='#DF420D',
                                popup='📍เขต: {} งบประมาณ: {} ล้านบาท'.format(row["เขต"], int(row['งบแผนงาน'] / 1000000)),
                                fill=True).add_to(folium_map)

    folium_map.save("budget_map.html")
