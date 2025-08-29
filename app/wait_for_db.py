import time
import logging
from sqlalchemy import text

import sys
sys.path.append("/app")

from app.database import engine, Base

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def wait_for_db():
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ База данных готова!", flush=True)
            break
        except Exception as e:
            print("⏳ Ожидание базы данных... Ошибка:", e)
            time.sleep(2)

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы созданы (или уже существуют)", flush=True)
    except Exception as e:
        print("❌ Ошибка при создании таблиц:", e)
        raise

if __name__ == "__main__":
    wait_for_db()