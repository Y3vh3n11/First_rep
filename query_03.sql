SELECT id_subject, AVG(grade) AS average_grade
FROM grades g
GROUP BY id_subject
ORDER BY id_subject desc;
