from time import sleep

import requests
import os
import pandas as pd
from datetime import datetime

# 配置数据保存路径
data_path = r'E:\pythonProject\crawler\dataset'
os.makedirs(data_path, exist_ok=True)

# API配置
url = "https://flk.npc.gov.cn/api/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Referer': 'https://flk.npc.gov.cn/'
}


def fetch_laws(page, size):
    params = {
        "type": "flfg",
        "searchType": "title;accurate",
        "sortTr": "f_bbrq_s;desc",
        "page": page,
        "sort": "true",
        "size": size,
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        # print(response.text)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None


def translate_status(status_code):
    status_mapping = {
        "1": "有效",
        "3": "尚未生效",
        "7": "",
    }
    return status_mapping.get(status_code, f"未知状态({status_code})")


def format_date(date_str):
    try:
        if date_str:
            return datetime.strptime(date_str.split()[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        return ""
    except:
        return date_str


# def parse_law_data(api_data):
#     if not api_data or not api_data.get("result", {}).get("data"):
#         return []
#
#     laws = []
#     for item in api_data["result"]["data"]:
#         laws.append({
#             '序号': item.get("id", ""),
#             '标题': item.get("title", ""),
#             '制定机关': item.get("office", ""),
#             '法律性质': item.get("type", ""),
#             '时效性': translate_status(item.get("status", "")),
#             '公布日期': format_date(item.get("publish", ""))
#         })
#     return laws

def parse_law_data(api_data, page):
    if not api_data or not api_data.get("result", {}).get("data"):
        return []

    laws = []
    for i, item in enumerate(api_data["result"]["data"], start=1):
        laws.append({
            '序号': i + (page-1) * 10,
            '标题': item.get("title", ""),
            '制定机关': item.get("office", ""),
            '法律性质': item.get("type", ""),
            '时效性': translate_status(item.get("status", "")),
            '公布日期': format_date(item.get("publish", ""))
        })
    return laws


def save_to_csv(data, filename="fl.csv"):
    if not data:
        print("无有效数据可保存")
        return

    filepath = os.path.join(data_path, filename)
    try:
        df = pd.DataFrame(data)
        # 检查文件是否存在，如果存在则追加数据，否则创建新文件
        if os.path.exists(filepath):
            df.to_csv(filepath, mode='a', index=False, header=False, encoding='utf-8-sig')
        else:
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
    except Exception as e:
        print(f"保存文件失败: {str(e)}")


def crawler(page):
    raw_data = fetch_laws(page=page, size=10)
    if not raw_data:
        print("获取数据失败，请检查网络或API状态")
        return

    laws_data = parse_law_data(raw_data, page)
    if not laws_data:
        print("未解析到有效数据")
        return

    # for i, law in enumerate(laws_data):
    #     i += 1
    #     print(f"序号: {i + (page-1) * 10}")
    #     print(f"标题: {law['标题']}")
    #     print(f"制定机关: {law['制定机关']}")
    #     print(f"法律性质: {law['法律性质']}")
    #     print(f"时效性: {law['时效性']}")
    #     print(f"公布日期: {law['公布日期']}")
    #     print('-' * 50)

    save_to_csv(laws_data)
    print(f"保存第{page}页数据")


if __name__ == "__main__":
    for pages in range(1, 71):
        crawler(pages)
        sleep(2)