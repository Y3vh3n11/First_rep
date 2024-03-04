select s."name" as subject, s2."name" as student , t."name" as teacher
from grades g 
join subjects s on g.id_subject = s.id 
join teachers t on s.id_teacher = t.id 
join students s2 on s2.id = g.id_student 
where g.id_student = 3
and t.id = 5
group by s."name", g.id_student , t."name" , s2."name"