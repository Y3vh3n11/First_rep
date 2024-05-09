from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.conf.config import settings

#  рядок з'єднання з базою даних.
SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
# створення двигуна engine.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# sessionmaker використовується для створення фабрики сесій, 
# яка використовується для створення сесій для взаємодії з базою даних. 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# залежність, яка повертає сесію з використанням фабрики SessionLocal. 
# Сесія закривається при виході з функції з використанням блоку finally.
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
