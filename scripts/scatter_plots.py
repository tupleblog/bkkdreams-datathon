"""
Scatter plot between
"""
import pandas as pd
import numpy as np
from numpy.random import random
from math import pi

from bokeh.io import output_notebook

output_notebook()
from bokeh.io import show, output_file
from bokeh.palettes import RdYlGn6
from bokeh.models import (
    BasicTicker,
    ColorBar,
    LinearColorMapper,
    PrintfTickFormatter,
    ColumnDataSource,
    HoverTool,
    Span,
)
from bokeh.plotting import figure, save, show, output_file
from bokeh.palettes import BuGn, Blues8, Oranges256


def plot_vs_population(districts_budget_df):
    """
    From district budget to scatter plots vs total population
    """
    for q in districts_budget_df.budget_type.unique():
        df = districts_budget_df.query("budget_type == '{}'".format(q))
        df["num_total"] = df["num_male"] + df["num_female"]
        df = df.groupby(["dname", "num_total"])["budget"].sum().reset_index()
        source = ColumnDataSource(
            data=dict(
                x=df["num_total"] / 10000, y=df["budget"] / 1000000, desc=df["dname"]
            )
        )
        p = figure(title="", tools="hover,box_zoom,reset")
        vline = Span(
            location=df.num_total.mean() / 10000,
            dimension="height",
            line_color="gold",
            line_width=1.5,
        )
        hline = Span(
            location=df["budget"].mean() / 1000000,
            dimension="width",
            line_color="gold",
            line_width=1.5,
        )
        p.circle(
            "x", "y", source=source, fill_alpha=0.2, size=10,
        )
        p.xaxis.axis_label = "จำนวนผู้อยู่อาศัย (หมื่นคน)"
        p.yaxis.axis_label = f"งบประมาณ{q} (ล้านบาท)"
        p.xaxis.axis_label_text_font_size = "15pt"
        p.yaxis.axis_label_text_font_size = "15pt"
        p.xaxis.major_label_text_font_size = "12pt"
        p.yaxis.major_label_text_font_size = "12pt"

        hover = HoverTool(
            tooltips=[
                ("เขต", "@desc"),
                (f"งบ{q}", "@y ล้านบาท"),
                ("จำนวนผู้อาศัย", "@x หมื่นคน"),
            ]
        )
        p.add_tools(hover)
        p.renderers.extend([vline, hline])
        output_file(f"plots/scatter-{q_map[q]}-budget.html", mode="inline")
        save(p)


def plot_vs_area(districts_budget_df):
    """
    From district budget to scatter plots vs area size
    """
    for q in districts_budget_df.budget_type.unique():
        df = districts_budget_df.query("budget_type == '{}'".format(q))
        df = df.groupby(["dname", "AREA"])["budget"].sum().reset_index()
        source = ColumnDataSource(
            data=dict(
                x=df["AREA"] / 1000000, y=df["budget"] / 1000000, desc=df["dname"]
            )
        )
        p = figure(title="", tools="hover,box_zoom,reset")
        vline = Span(
            location=df.AREA.mean() / 1000000,
            dimension="height",
            line_color="gold",
            line_width=1.5,
        )
        hline = Span(
            location=df["budget"].mean() / 1000000,
            dimension="width",
            line_color="gold",
            line_width=1.5,
        )

        p.circle(
            "x", "y", source=source, fill_alpha=0.2, size=10,
        )

        p.xaxis.axis_label = "ขนาดพื้นที่ (ตร.กม.)"
        p.yaxis.axis_label = f"งบประมาณ{q} (ล้านบาท)"
        p.xaxis.axis_label_text_font_size = "15pt"
        p.yaxis.axis_label_text_font_size = "15pt"
        p.xaxis.major_label_text_font_size = "12pt"
        p.yaxis.major_label_text_font_size = "12pt"

        hover = HoverTool(
            tooltips=[
                ("เขต", "@desc"),
                (f"งบ{q}", "@y ล้านบาท"),
                ("ขนาดพื้นที่", "@x ตร.กม."),
            ]
        )
        p.add_tools(hover)
        p.renderers.extend([vline, hline])
        output_file(f"plots/scatter-{q_map[q]}-budget-area.html", mode="inline")
        save(p)


if __name__ == "__main__":
    districts_budget_df = pd.read_csv("data/districts_budget.csv")[
        ["dname", "ประเภทแผนงาน", "งบแผนงาน", "AREA", "num_male", "num_female"]
    ]
    districts_budget_df["num_total"] = (
        districts_budget_df.num_male + districts_budget_df.num_female
    )
    districts_budget_df.rename(
        columns={"ประเภทแผนงาน": "budget_type", "งบแผนงาน": "budget"}, inplace=True
    )

    q_map = {
        "ทั่วไป/บริหาร/อื่นๆ": "gen",
        "การคลัง": "treasury",
        "เทศกิจ/รักษาความสะอาด": "clean",
        "โยธา/ก่อสร้าง/จราจร": "civil",
        "น้ำท่วม/ทางเท้า": "pedes",
        "สิ่งแวดล้อม": "env",
        "พัฒนาชุมชน/อาชีพ": "enh",
        "อนามัย/สาธารณะสุข": "health",
        "การศึกษา": "edu",
    }
    plot_vs_population(districts_budget_df)
    plot_vs_area(districts_budget_df)
