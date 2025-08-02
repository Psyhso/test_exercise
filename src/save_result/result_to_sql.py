import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from parser.parser import parser


Base = declarative_base()


class Tender(Base):
    __tablename__ = 'tenders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tender_number = Column(Integer, unique=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    tender_name = Column(String(500))
    tender_url = Column(String(500))
    start_price = Column(Integer)
    city = Column(String(100))

    def __repr__(self):
        return f"<Tender({self.tender_number}: {self.tender_name})>"


def save_to_sql(count, db_path='sqlite:///tenders.db'):
    tenders_data = parser(count)
    if isinstance(tenders_data, str) and tenders_data.startswith("Ошибка"):
        print(tenders_data)
        return False

    try:
        df = pd.DataFrame(tenders_data)

        column_mapping = {
            'Номер тендера': 'tender_number',
            'Название тендера': 'tender_name',
            'Начало торгов': 'start_date',
            'День окончания торгов': 'end_date',
            'Начальная цена': 'start_price',
            'Город': 'city',
            'Ссылка на тендер': 'tender_url'
        }
        df = df.rename(columns=column_mapping)

        engine = create_engine(db_path)

        inspector = inspect(engine)
        if not inspector.has_table('tenders'):
            Base.metadata.create_all(engine)

        df.to_sql(
            name='tenders',
            con=engine,
            if_exists='replace',
            index=False,
            dtype={
                'tender_number': Integer(),  # Используем SQLAlchemy Integer
                'tender_name': String(500),
                'start_date': DateTime(),
                'end_date': DateTime(),
                'start_price': Integer(),
                'city': String(100),
                'tender_url': String(500)
            }
        )
        print(f"Успешно сохранено {len(df)} тендеров в базу данных")
        return True

    except Exception as e:
        print(f"Ошибка при сохранении: {str(e)}")
        return False
