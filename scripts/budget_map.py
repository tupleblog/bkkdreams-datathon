import json

# import os.path as op
import pandas as pd
import folium


if __name__ == "__main__":
    budget_total_df = pd.read_csv("../data/districts_total_budget.csv")
    df_thai_address_data = pd.read_csv("../data/thai_address_data.csv")
    lat_long_df = (
        df_thai_address_data.query("province == 'กรุงเทพมหานคร'")
        .groupby("district")[["latitude", "longitude"]]
        .mean()
        .reset_index()
    )

    lat_long_df["district"] = lat_long_df.district.map(
        lambda x: x.replace("ราษฎร์บูรณะ", "ราษฎร์บูรณะ").strip()
    )
    budget_total_df["dname"] = budget_total_df.dname.map(lambda x: x.strip())
    budget_total_df = (
        budget_total_df[["dname", "งบแผนงาน"]]
        .rename(columns={"dname": "district"})
        .merge(lat_long_df)
    )

    folium_map = folium.Map(
        location=[13.738, 100.597], zoom_start=11, tiles="Stamen Toner"
    )

    for _, row in budget_total_df.iterrows():
        if row["latitude"] != "":
            folium.CircleMarker(
                location=(row["latitude"], row["longitude"]),
                radius=row["งบแผนงาน"] / 30000000,
                color="#DF420D",
                popup="📍เขต: {} งบประมาณ: {} ล้านบาท".format(
                    row["district"], int(row["งบแผนงาน"] / 1000000)
                ),
                fill=True,
            ).add_to(folium_map)

    folium_map.save("../plots/budget_map.html")
