from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#  рядок з'єднання з базою даних.
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432"
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
