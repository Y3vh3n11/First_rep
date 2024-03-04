from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

def create_table(cur):
    with open('create_table.sql', 'r') as file:
        create = file.read()
    
    cur.execute(create)


def insert_data(cur):
    # Додавання груп
    for _ in range(3):
        cur.execute("INSERT INTO groups (name) VALUES (%s)", (fake.safe_color_name(),))
    # Додавання викладачів
    for _ in range(5):
        cur.execute('INSERT INTO teachers (name) VALUES (%s)', (fake.name(), ))
    # Додавання предметів
    for id_teacher in range(1,6):
        for _ in range(2):
            cur.execute('INSERT INTO subjects (name, id_teacher) VALUES (%s, %s)', (fake.word(), id_teacher))
    # Додавання студентів і оцінок
    for id_group in range(1,4):
        for _ in range(15):
            cur.execute('INSERT INTO students (name, id_group) VALUES (%s,%s)  RETURNING id', (fake.name(), id_group))
            id_student = cur.fetchone()[0]
            for id_subject in range(1, 11):
                for _ in range(3):
                    cur.execute("INSERT INTO grades (id_student, id_subject, grade, grade_date) VALUES (%s, %s, %s, %s)",
                                (id_student, id_subject, random.randint(0, 100), fake.date_this_decade()))


def select_sql(cur):
    tests = ['query_01.sql','query_02.sql','query_03.sql','query_04.sql','query_05.sql','query_06.sql','query_07.sql','query_08.sql','query_09.sql','query_10.sql',]
    for test in tests:
        with open(test, 'r') as file:
            cmd = file.read()
        cur.execute(cmd)
        res = cur.fetchall()
        print('\n')
        for i in res:
            print(i)

if __name__ == '__main__':
    try:
        # Підключення до бази даних
        conn = psycopg2.connect(host="localhost", database="test_les2", user="postgres", password="1")
        cur = conn.cursor()
    
        create_table(cur) # створення таблиць
        insert_data(cur) # заповнення таблиць
        
        # select_sql(cur) # для запуску тестових запитів
        
        # Збереження змін
        conn.commit()
    except DatabaseError as e:
        print(e)
        conn.rollback()
    finally:
        # Закриття підключення
        cur.close()
        conn.close()
