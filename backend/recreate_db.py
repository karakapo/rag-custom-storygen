from database import db
from models import Base
from sqlalchemy import text

def recreate_database():
    with db._engine.connect() as conn:
        # Mevcut tabloları sil
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()
        
        # Tabloları yeniden oluştur
        Base.metadata.create_all(bind=db._engine)
        print("Veritabanı başarıyla yeniden oluşturuldu!")

if __name__ == "__main__":
    recreate_database() 