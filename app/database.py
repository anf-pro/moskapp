from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# معلومات الاتصال بقاعدة البيانات
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# إنشاء محرك الاتصال
engine = create_engine(DATABASE_URL)

# إنشاء جلسة للتعامل مع قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء القاعدة الأساسية لكل الموديلات
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
