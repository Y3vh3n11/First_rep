from faker import Faker
import random
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session

fake = Faker()

def insert_data():
    # Додавання груп
    for _ in range(3):
        new_group = Group(name = fake.safe_color_name())
        session.add(new_group)
    
    # Додавання викладачів
    for _ in range(5):
        new_teacher = Teacher(fullname=fake.name())
        session.add(new_teacher)
        
    # Додавання предметів
    for id_teacher in range(1,6):
        for _ in range(2):
            new_subj = Subject(name=fake.word(), teacher_id=id_teacher)
            session.add(new_subj)

    # Додавання студентів і оцінок
    for id_group in range(1,4):
        for id_stud in range(1, 16):
            new_student = Student(fullname=fake.name(), group_id=id_group)
            session.add(new_student)
            for id_subject in range(1, 11):
                for _ in range(3):
                    new_grades = Grade(grade=random.randint(0, 100), grade_date=fake.date_this_decade(), student_id= id_stud, subject_id=id_subject)
                    session.add(new_grades)
    
if __name__ == '__main__':
    insert_data() # заповнення таблиць
    session.commit()
    
        