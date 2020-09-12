from flask import Flask, Response, jsonify
from dotenv import load_dotenv, find_dotenv
from cachetools import cached, LRUCache, TTLCache
from airtable import Airtable
from collections import Counter
from cachetools import TTLCache

import pandas as pd
import requests
import os

load_dotenv(find_dotenv())

print("Starting Server")

AIRTABLE_ID = os.getenv("AIRTABLE_ID")
AIRTABLE_KEY = os.getenv("AIRTABLE_KEY")

app = Flask(__name__)


def get_airtable_data(table_name: str):
    """
    Get data from Airtable with a particular AIRTABLE_ID
    stated in .env file in this directory

    table_name can be ``talks``, ``jobboard``, ``jobseeker``
    """

    request_url = f"https://api.airtable.com/v0/{AIRTABLE_ID}/{table_name}?api_key={AIRTABLE_KEY}"
    print(request_url)
    airtable_data = requests.get(request_url).json()
    return airtable_data


def format_dict_counter(dict_counter):
    """
    Format dictionary and rank by sum
    """
    result = []
    for k, v in sorted(dict_counter.items(), key=lambda item: item[1], reverse=True):
        result.append({"budget_type": k, "amount": v})
    return result


# cache for 1 minute
@cached(cache=TTLCache(maxsize=32, ttl=60))
def get_survey_df():

    # survey = get_airtable_data("survey")
    # survey_df = pd.DataFrame([r["fields"] for r in survey["records"]])

    survey_table = Airtable(AIRTABLE_ID, "survey", AIRTABLE_KEY)
    survey = survey_table.get_all()

    survey_df = pd.DataFrame([r["fields"] for r in survey])

    # Fill null value with empty list
    for row in survey_df.loc[survey_df.decrease_list.isnull(), "decrease_list"].index:
        survey_df.at[row, "decrease_list"] = []

    for row in survey_df.loc[survey_df.increase_list.isnull(), "increase_list"].index:
        survey_df.at[row, "increase_list"] = []

    return survey_df


def get_data_district():

    survey_df = get_survey_df()
    survey_summary_df = survey_df.groupby("district").agg(sum).reset_index()

    survey_summary_df["to_increase"] = survey_summary_df["increase_list"].map(
        lambda x: format_dict_counter(dict(Counter(x)))
    )
    survey_summary_df["to_decrease"] = survey_summary_df["decrease_list"].map(
        lambda x: format_dict_counter(dict(Counter(x)))
    )
    result = survey_summary_df[["district", "to_increase", "to_decrease"]].to_dict(orient="records")

    # Add more data
    for r in result:
        r["sum_to_increase"] = sum([x["amount"] for x in r["to_increase"]])
        r["sum_to_decrease"] = sum([x["amount"] for x in r["to_decrease"]])

    return result


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def api_survey(path):

    survey_df = get_survey_df()

    sex_count = survey_df["sex"].value_counts().to_dict()

    print(survey_df.info())

    survey_amount = survey_df.shape[0]

    data_district = get_data_district()

    # budget_type count
    budget_increase = {}
    budget_decrease = {}
    for d in data_district:
        for ti in d["to_increase"]:
            budget_type = ti["budget_type"]

            if budget_type not in budget_increase.keys():
                budget_increase[budget_type] = 0

            budget_increase[budget_type] += ti["amount"]

        for ti in d["to_decrease"]:
            budget_type = ti["budget_type"]

            if budget_type not in budget_decrease.keys():
                budget_decrease[budget_type] = 0

            budget_decrease[budget_type] += ti["amount"]

    budget_increases = [
        {"budget_type": k, "amount": v}
        for k, v in sorted(budget_increase.items(), key=lambda item: item[1], reverse=True)
    ]
    budget_decreases = [
        {"budget_type": k, "amount": v}
        for k, v in sorted(budget_decrease.items(), key=lambda item: item[1], reverse=True)
    ]

    data = {
        "v": "0.0.1",
        "status": True,
        "data_district": data_district,
        "survey_amount": survey_amount,
        "sex_count": sex_count,
        "budget_increases": budget_increases,
        "budget_decreases": budget_decreases,
    }

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5003)
