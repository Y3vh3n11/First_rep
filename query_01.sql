select s.id, s.name, AVG(g.grade) as avg_grade
from students s
join grades g on s.id = g.id_student
group by s.id
order  by avg_grade desc 
limit 5;
