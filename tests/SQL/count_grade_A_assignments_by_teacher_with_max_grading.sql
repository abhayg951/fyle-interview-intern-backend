-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH graded_assignments AS (
    SELECT teacher_id, COUNT(*) AS num_graded_assignments
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
), max_grading_teacher AS (
    SELECT teacher_id
    FROM graded_assignments
    ORDER BY num_graded_assignments DESC
    LIMIT 1
)
SELECT COUNT(*) AS num_grade_A_assignments
FROM assignments
WHERE state = 'GRADED'
    AND grade = 'A'
    AND teacher_id = (SELECT teacher_id FROM max_grading_teacher);