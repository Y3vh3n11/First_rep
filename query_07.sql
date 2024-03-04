SELECT id_student, s.name as student, grade, s2.name as subject, s.id_group as group
FROM grades g 
join students s on g.id_student = s.id 
join subjects s2 on g.id_subject = s2.id 
WHERE id_subject = 6
and s.id_group = 2