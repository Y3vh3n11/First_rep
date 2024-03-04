select id_student, s."name" as student , id_subject , s2."name" as subject 
from grades g 
join students s on g.id_student = s.id 
join subjects s2 on g.id_subject = s2.id 
where id_student = 2
group by id_student, s."name" , id_subject , s2."name"  
order by id_subject 