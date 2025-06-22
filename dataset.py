import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd


def parse_characteristics(paragraphs):
    result = {}

    for item in paragraphs:
        if ":" in item:
            key, value = item.split(":", 1)
            result[key.strip()] = value.strip()
        else:
            
            result["Тип продавца"] = item.strip()

    return result

def split_date_location(date_loc):
    try:
        
        full_loc, date_part = date_loc.split(" - ", 1)
        if "Ташкент," in full_loc:
            location = full_loc.replace("Ташкент,", "").strip()
        else:
            location = full_loc.strip()
        return location, date_part.strip()
    except:
        return None, None  


all_combined = []  

for count in range(1, 25):
    url = f'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/?currency=UZS&page={count}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find_all("div", class_='css-u2ayx9')
    data_1 = soup.find_all("div", class_='css-odp1qd')
    DATA1 = []

    for i, l in zip(data, data_1):
        try:
            name = i.find('h4', class_='css-1g61gc2').text.strip()
            price = i.find('p', class_='css-uj7mm0').text
            price = re.sub(r"[^\d.]", "", price)
            price = float(price)
            ahref = i.find('a', class_='css-1tqlkj0').get("href")
            ahref = f'https://www.olx.uz{ahref}'

            date_loc = l.find('p', class_='css-vbz67q').text
            loc, date = split_date_location(date_loc)

            DATA1.append({
                'Название': name,
                'Цена': price,
                'Линк': ahref,
                'Местоположение': loc,
                'Дата': date
            })
        except Exception as e:
            print("Ошибка при извлечении блока:", e)
            continue

    DATA2 = []

    for item in DATA1:
        try:
            response1 = requests.get(item['Линк'], timeout=10)
            soup1 = BeautifulSoup(response1.text, 'lxml')
            data1_blocks = soup1.find_all("div", class_='css-41yf00')

            full_characteristics = {}

            for block in data1_blocks:
                paragraphs = block.find_all('p', class_='css-1los5bp')
                paragraphs = [p.text.strip() for p in paragraphs]
                parsed = parse_characteristics(paragraphs)
                full_characteristics.update(parsed)

            DATA2.append(full_characteristics)
        except Exception as e:
            print("Ошибка при загрузке деталей:", e)
            DATA2.append({})  

    for base, details in zip(DATA1, DATA2):
        merged = {**base, **details}
        all_combined.append(merged)


df = pd.DataFrame(all_combined)
df.to_csv("full_olx_dataset.csv", index=False, encoding='utf-8-sig')
print(f"[✔] Сохранено {len(df)} объявлений в 'full_olx_dataset.csv'")
