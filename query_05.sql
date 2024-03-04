select t.id, t.name, s.name as subject
from teachers t 
join subjects s on t.id = s.id_teacher 
group by t.id, subject 
order by t.id