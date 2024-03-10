from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session
from sqlalchemy import func, desc

def select_01():
# select s.id, s.fullname, AVG(g.grade) as avg_grade
# from students s
# join grades g on s.id = g.student_id
# group by s.id
# order  by avg_grade desc 
# limit 5;

    res = session.query(Student.id, Student.fullname, func.avg(Grade.grade).label('avg_grade'))\
    .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return res


def select_02():
# select s.id, s.fullname, avg(g.grade) as grade
# from grades g 
# join students s on s.id = g.student_id
# where g.subject_id = 5
# group by s.id
# order by grade desc
# limit 1;
    
    res = session.query(Student.id, Student.fullname, func.AVG(Grade.grade).label('avg_grade'))\
    .select_from(Grade).join(Student).filter(Grade.subject_id == 5).group_by(Student.id)\
    .order_by(desc('avg_grade')).limit(1).all()
    return res

def select_03():
# SELECT g.subject_id, AVG(grade) AS avg_grade
# FROM grades g
# GROUP BY subject_id
# ORDER BY subject_id desc;
    res = session.query(Grade.subject_id, func.AVG(Grade.grade).label('avg_grade'))\
    .select_from(Grade).group_by(Grade.subject_id).order_by(desc(Grade.subject_id)).all()
    return res

def select_04():
# select avg(grade) as avggrade
# from grades g 
    res = session.query(func.AVG(Grade.grade).label('avg_grade')).select_from(Grade).all()
    return res

def select_05():
# select t.id, t.fullname, s.name as subject
# from teachers t 
# join subjects s on t.id = s.teacher_id 
# group by t.id, subject 
# order by t.id
    res = session.query(Teacher.id, Teacher.fullname, Subject.name.label('subject')).select_from(Teacher)\
    .join(Subject).group_by(Teacher.id, Subject.name).order_by(Teacher.id).all()
    return res
    
def select_06():
# select s.id, s.fullname, s.group_id
# from students s
# where group_id = 1;
    res = session.query(Student.id, Student.fullname, Student.group_id).select_from(Student)\
    .where(Student.group_id == 1).all()
    return res
    

def select_07():
# SELECT g.student_id, s.fullname as student, grade, s2.name as subject, s.group_id as group
# FROM grades g 
# join students s on g.student_id = s.id 
# join subjects s2 on g.subject_id = s2.id 
# WHERE subject_id = 1
# and s.group_id = 1
    res = session.query(Grade.student_id, Student.fullname.label('student'),\
    Grade.grade, Subject.name, Student.group_id.label('group')).select_from(Grade)\
    .join(Student).join(Subject).where(Subject.id == 1).where(Student.group_id == 1).all()
    return res

def select_08():
# select avg(g.grade) as avg_grade, s."name" as subject ,t.fullname  
# from grades g 
# join subjects s on g.subject_id  = s.id 
# join teachers t on s.teacher_id  = t.id 
# where s.teacher_id  = 3
# GROUP by s."name", t.fullname 
    res = session.query(func.AVG(Grade.grade).label('avg_grade'), Subject.name.label('subject'), Teacher.fullname)\
    .select_from(Grade).join(Subject).join(Teacher).where(Subject.teacher_id == 3)\
    .group_by(Subject.name, Teacher.fullname).all()
    return res
    

def select_09():
# select g.student_id, s.fullname as student , g.subject_id  , s2."name"  as subject 
# from grades g 
# join students s on g.student_id = s.id 
# join subjects s2 on g.subject_id = s2.id 
# where student_id = 2
# group by student_id, s.fullname , subject_id , s2."name"  
# order by subject_id
    res = session.query(Grade.student_id, Student.fullname.label('student'), Grade.subject_id, Subject.name.label('subject'))\
    .select_from(Grade).join(Student).join(Subject).where(Grade.student_id == 2)\
    .group_by(Grade.student_id, Student.fullname, Grade.subject_id, Subject.name)\
    .order_by(Grade.subject_id).all()
    return res


def select_10():
# select s."name" as subject, s2.fullname  as student , t.fullname  as teacher
# from grades g 
# join subjects s on g.subject_id  = s.id 
# join teachers t on s.teacher_id  = t.id 
# join students s2 on s2.id = g.student_id  
# where g.student_id = 3
# and t.id = 5
# group by s."name", g.student_id , t.fullname , s2.fullname
    res = session.query(Subject.name.label('subject'), Student.fullname, Teacher.fullname.label('teacher'))\
    .select_from(Grade).join(Subject).join(Teacher).join(Student).where(Grade.student_id == 3).where(Teacher.id == 5)\
    .group_by(Subject.name, Grade.student_id, Teacher.fullname, Student.fullname).all()
    return res

if __name__ == '__main__':
    print('\n'*2, f'select_01():\n{select_01()}', '\n'*2)
    print('\n'*2, f'select_02():\n{select_02()}', '\n'*2)
    print('\n'*2, f'select_03():\n{select_03()}', '\n'*2)
    print('\n'*2, f'select_04():\n{select_04()}', '\n'*2)
    print('\n'*2, f'select_05():\n{select_05()}', '\n'*2)
    print('\n'*2, f'select_06():\n{select_06()}', '\n'*2)
    print('\n'*2, f'select_07():\n{select_07()}', '\n'*2)
    print('\n'*2, f'select_08():\n{select_08()}', '\n'*2)
    print('\n'*2, f'select_09():\n{select_09()}', '\n'*2)
    print('\n'*2, f'select_10():\n{select_10()}', '\n'*2)
