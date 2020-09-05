import json
# import os.path as op
import pandas as pd
import folium


if __name__ == "__main__":
    df_budget_district_agg = pd.read_csv('../data/budget_district_info.csv'
                                        ).dropna(subset=['dname']
                                                ).groupby('dname')['งบแผนงาน'].sum().reset_index().rename(columns={'dname':'เขต'})

    df_thai_address_data = pd.read_csv('../data/thai_address_data.csv')
    budget_sum_df = df_thai_address_data.loc[df_thai_address_data.province=='กรุงเทพมหานคร'
                                            ].rename(columns={'district':'เขต'}
                                                    ).merge(df_budget_district_agg, on='เขต', how='left'
                                                           ).groupby('เขต')[['latitude','longitude','งบแผนงาน']].mean().dropna().reset_index()
    
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
