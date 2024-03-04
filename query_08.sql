select avg(g.grade) as avggrade, s."name" as subject ,t."name" 
from grades g 
join subjects s on g.id_subject = s.id 
join teachers t on s.id_teacher = t.id 
where s.id_teacher = 3
GROUP by s."name", t."name" 