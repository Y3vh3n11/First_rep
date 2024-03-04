select s.id, s.name, avg(g.grade) as grade
from grades g 
join students s on s.id = g.id_student
where g.id_subject = 5
group by s.id
order by grade desc
limit 1;