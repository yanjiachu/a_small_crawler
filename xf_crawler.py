import requests
import os
import pandas as pd
from bs4 import BeautifulSoup

data_path = 'E:\pythonProject\crawler\dataset'
url = 'https://flk.npc.gov.cn/xf.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
html  = response.text
soup = BeautifulSoup(html, 'html.parser')
tbody = soup.find('tbody', {'id': 'flData'})

laws = []

# 遍历每一行tr
for tr in tbody.find_all('tr', class_='list-b'):
    # 提取序号
    serial_number = tr.find('div', class_='l-xh').text.strip()
    serial_number = int(serial_number)

    # 提取标题
    title = tr.find('li', class_='l-wen').text.strip()

    # 提取制定机关
    issuing_authority = tr.find('td', class_='l-sx2').find('h2', class_='l-wen1').text.strip()

    # 提取法律性质（有多个l-sx3类，取第一个）
    law_type = tr.find_all('td', class_='l-sx3')[0].find('h2', class_='l-wen1').text.strip()

    # 提取时效性（有多个l-sx3类，取第二个）
    validity = tr.find_all('td', class_='l-sx3')[1].find('h2', class_='l-wen1').text.strip()

    # 提取公布日期，取[1:10]位置的字符串
    publish_date = tr.find('td', class_='l-sx4').find('h2', class_='l-wen1').text.strip()[1:10]

    # 将数据存入字典
    law_data = {
        '序号': serial_number,
        '标题': title,
        '制定机关': issuing_authority,
        '法律性质': law_type,
        '时效性': validity,
        '公布日期': publish_date
    }

    laws.append(law_data)

# for law in laws:
#     print(f"序号: {law['序号']}")
#     print(f"标题: {law['标题']}")
#     print(f"制定机关: {law['制定机关']}")
#     print(f"法律性质: {law['法律性质']}")
#     print(f"时效性: {law['时效性']}")
#     print(f"公布日期: {law['公布日期']}")
#     print('-' * 50)

filepath = os.path.join(data_path, "xf.csv")
try:
    df = pd.DataFrame(laws)
    # 检查文件是否存在，如果存在则追加数据，否则创建新文件
    if os.path.exists(filepath):
        df.to_csv(filepath, mode='a', index=False, header=False, encoding='utf-8-sig')
    else:
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"保存文件失败: {str(e)}")