import os
import json
import requests
import random
from tqdm import tqdm_notebook
from dotenv import load_dotenv

load_dotenv(verbose=True)

AIRTABLE_ID = os.environ.get("AIRTABLE_ID")
AIRTABLE_KEY = os.environ.get("AIRTABLE_KEY")


possible_types = [
    "งานทั่วไป",
    "การศึกษา",
    "สิ่งแวดล้อม",
    "เทศกิจ/รักษาความสะอาด",
    "น้ำท่วม/ทางเท้า",
    "โรงพยาบาล/แพทย์",
    "อนามัย/สาธารณะสุข",
    "พัฒนาชุมชน/อาชีพ",
    "ขนส่งสาธารณะ",
    "การคลัง"
]

possible_age = [
    "10 - 20 ปี",
    "21 - 30 ปี",
    "31 - 40 ปี",
    "41 - 50 ปี",
    "51 - 60 ปี",
    "> 60 ปี",
]

possible_sex = ["ชาย", "หญิง", "เพศท่ีสาม", "ไม่ประสงค์จะระบุ"]

possible_district = [
    "ทวีวัฒนา",
    "หนองแขม",
    "พระนคร",
    "ดุสิต",
    "หนองจอก",
    "บางรัก",
    "บางเขน",
    "บางกะปิ",
    "ปทุมวัน",
    "ป้อมปราบศัตรูพ่าย",
    "พระขโนง",
    "มีนบุรี",
    "ลาดกระบัง",
    "ยานนาวา",
    "สัมพันธวงศ์",
    "พญาไท",
    "ธนบุรี",
    "บางกอกใหญ่",
    "ห้วงขวาง",
    "คลองสาน",
    "ตลิ่งชัน",
    "บางกอกน้อย",
    "บางขุนเทียน",
    "ภาษีเจริญ",
    "ราษฎร์บูรณะ",
    "บางพลัด",
    "ดินแดง",
    "บึงกุ่ม",
    "สาทร",
    "บางซื่อ",
    "จตุจักร",
    "บางคอแหลม",
    "ประเวศ",
    "คลองเตย",
    "สวนหลวง",
    "จอมทอง",
    "ดอนเมือง",
    "ราชเทวี",
    "ลาดพร้าว",
    "วัฒนา",
    "บางแค",
    "หลักสี่",
    "สายไหม",
    "คันนายาว",
    "สะพานสูง",
    "วังทองหลาง",
    "คลองสามวา",
    "บางนา",
    "บางนาใต้",
    "ทุ่งครุ",
    "บางบอน",
]


def chunks(l, n):
    """
    Yield successive n-sized chunks from list ``l``.
    """
    for i in range(0, len(l), n):
        yield l[i : i + n]


def gen_sample_data(n_sample=300):
    """
    Generate sample data
    """
    survey_data = []
    for _ in tqdm_notebook(range(n_sample)):
        district = random.choice(possible_district)
        age = random.choice(possible_age)
        sex = random.choice(possible_sex)
        increase_list = random.sample(
            possible_types, random.randint(1, len(possible_types) - 2)
        )
        decrease_list = random.sample(
            list(set(possible_types) - set(increase_list)), random.randint(1, 2)
        )
        survey_data.append(
            {
                "district": district,
                "increase_list": increase_list,
                "decrease_list": decrease_list,
                "age": age,
                "sex": sex,
            }
        )
    return survey_data


def set_data_airtable(data: list, table_name: str = "survey"):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json",
    }
    results = []
    data_slices = list(chunks(data, 10))
    for data_slice in tqdm_notebook(data_slices):
        data = {"records": [{"fields": d} for d in data_slice]}
        post_url = f"https://api.airtable.com/v0/{AIRTABLE_ID}/{table_name}"
        output = requests.post(post_url, data=json.dumps(data), headers=headers)
        results.append(output.json())
    return results


if __name__ == "__main__":
    sample_survey_data = gen_sample_data(n_sample=300)
    results = set_data_airtable(sample_survey_data)
    print(results)