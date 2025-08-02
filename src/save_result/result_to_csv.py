import pandas as pd
from parser.parser import parser


def save_to_csv(count, path):
    tenders_data = parser(count)

    if isinstance(tenders_data, str) and tenders_data.startswith("Ошибка"):
        print(tenders_data)
    else:
        df = pd.DataFrame(tenders_data)
        df.to_csv(f"{path}", index=False, encoding='utf-8-sig')
        print("Данные успешно сохранены в tenders.csv")
