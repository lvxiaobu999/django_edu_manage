# 考试模拟数据 SQL

> **学期**：2025-2026 学年第一学期（semester_id=3）  
> **满分**：100 分 | **随机范围**：40.0 ~ 100.0（保留 1 位小数）  
> **策略**：INSERT INTO ... SELECT 批量生成，避免逐行 VALUES。

## 目录

1. [考试计划](#一考试计划-exam_plan)  
2. [成绩数据](#二成绩数据-score)  
3. [数据量统计](#三数据量统计)

---

## 一、考试计划（exam_plan）

```sql
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (1, '2025-2026学年第一学期一年级期中考试', 'MIDTERM', '2025-11-01', 'GRADE_1', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (2, '2025-2026学年第一学期一年级期末考试', 'FINAL', '2026-01-01', 'GRADE_1', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (3, '2025-2026学年第一学期二年级期中考试', 'MIDTERM', '2025-11-02', 'GRADE_2', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (4, '2025-2026学年第一学期二年级期末考试', 'FINAL', '2026-01-02', 'GRADE_2', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (5, '2025-2026学年第一学期三年级期中考试', 'MIDTERM', '2025-11-03', 'GRADE_3', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (6, '2025-2026学年第一学期三年级期末考试', 'FINAL', '2026-01-03', 'GRADE_3', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (7, '2025-2026学年第一学期四年级期中考试', 'MIDTERM', '2025-11-04', 'GRADE_4', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (8, '2025-2026学年第一学期四年级期末考试', 'FINAL', '2026-01-04', 'GRADE_4', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (9, '2025-2026学年第一学期五年级期中考试', 'MIDTERM', '2025-11-05', 'GRADE_5', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (10, '2025-2026学年第一学期五年级期末考试', 'FINAL', '2026-01-05', 'GRADE_5', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (11, '2025-2026学年第一学期六年级期中考试', 'MIDTERM', '2025-11-06', 'GRADE_6', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (12, '2025-2026学年第一学期六年级期末考试', 'FINAL', '2026-01-06', 'GRADE_6', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (13, '2025-2026学年第一学期七年级期中考试', 'MIDTERM', '2025-11-11', 'GRADE_7', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (14, '2025-2026学年第一学期七年级期末考试', 'FINAL', '2026-01-11', 'GRADE_7', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (15, '2025-2026学年第一学期八年级期中考试', 'MIDTERM', '2025-11-12', 'GRADE_8', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (16, '2025-2026学年第一学期八年级期末考试', 'FINAL', '2026-01-12', 'GRADE_8', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (17, '2025-2026学年第一学期九年级期中考试', 'MIDTERM', '2025-11-13', 'GRADE_9', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (18, '2025-2026学年第一学期九年级期末考试', 'FINAL', '2026-01-13', 'GRADE_9', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (19, '2025-2026学年第一学期高一模拟考试', 'MOCK', '2025-10-21', 'SENIOR_1', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (20, '2025-2026学年第一学期高一月考试', 'MONTHLY', '2025-12-21', 'SENIOR_1', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (21, '2025-2026学年第一学期高二模拟考试', 'MOCK', '2025-10-22', 'SENIOR_2', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (22, '2025-2026学年第一学期高二月考试', 'MONTHLY', '2025-12-22', 'SENIOR_2', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (23, '2025-2026学年第一学期高三模拟考试', 'MOCK', '2025-10-23', 'SENIOR_3', 3);
INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id) VALUES (24, '2025-2026学年第一学期高三月考试', 'MONTHLY', '2025-12-23', 'SENIOR_3', 3);
```

| 学段 | 年级 | 考试类型 | 日期 | 科目 |
|------|------|----------|------|------|
| 小学 | 一年级 | 期中 | 2025-11-01 | 语文、数学、英语 |
| 小学 | 一年级 | 期末 | 2026-01-01 | 语文、数学、英语 |
| 小学 | 二年级 | 期中 | 2025-11-02 | 语文、数学、英语 |
| 小学 | 二年级 | 期末 | 2026-01-02 | 语文、数学、英语 |
| 小学 | 三年级 | 期中 | 2025-11-03 | 语文、数学、英语 |
| 小学 | 三年级 | 期末 | 2026-01-03 | 语文、数学、英语 |
| 小学 | 四年级 | 期中 | 2025-11-04 | 语文、数学、英语 |
| 小学 | 四年级 | 期末 | 2026-01-04 | 语文、数学、英语 |
| 小学 | 五年级 | 期中 | 2025-11-05 | 语文、数学、英语 |
| 小学 | 五年级 | 期末 | 2026-01-05 | 语文、数学、英语 |
| 小学 | 六年级 | 期中 | 2025-11-06 | 语文、数学、英语 |
| 小学 | 六年级 | 期末 | 2026-01-06 | 语文、数学、英语 |
| 初中 | 七年级 | 期中 | 2025-11-11 | 语文、数学、英语、物理、化学、政治、历史、地理、体育 |
| 初中 | 七年级 | 期末 | 2026-01-11 | 语文、数学、英语、物理、化学、政治、历史、地理、体育 |
| 初中 | 八年级 | 期中 | 2025-11-12 | 语文、数学、英语、物理、化学、政治、历史、地理、体育 |
| 初中 | 八年级 | 期末 | 2026-01-12 | 语文、数学、英语、物理、化学、政治、历史、地理、体育 |
| 初中 | 九年级 | 期中 | 2025-11-13 | 语文、数学、英语、物理、化学、政治、历史、地理、体育 |
| 初中 | 九年级 | 期末 | 2026-01-13 | 语文、数学、英语、物理、化学、政治、历史、地理、体育 |
| 高中 | 高一 | 模拟考 | 2025-10-21 | 语文、数学、英语、物理、化学、生物、政治、历史、地理、体育 |
| 高中 | 高一 | 月考 | 2025-12-21 | 语文、数学、英语、物理、化学、生物、政治、历史、地理、体育 |
| 高中 | 高二 | 模拟考 | 2025-10-22 | 语文、数学、英语、物理、化学、生物、政治、历史、地理、体育 |
| 高中 | 高二 | 月考 | 2025-12-22 | 语文、数学、英语、物理、化学、生物、政治、历史、地理、体育 |
| 高中 | 高三 | 模拟考 | 2025-10-23 | 语文、数学、英语、物理、化学、生物、政治、历史、地理、体育 |
| 高中 | 高三 | 月考 | 2025-12-23 | 语文、数学、英语、物理、化学、生物、政治、历史、地理、体育 |

---

## 二、成绩数据（score）

### 小学

```sql
-- 一年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 1, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_1';
-- 一年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 1, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_1';
-- 一年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 1, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_1';
-- 一年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 2, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_1';
-- 一年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 2, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_1';
-- 一年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 2, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_1';
-- 二年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 3, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_2';
-- 二年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 3, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_2';
-- 二年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 3, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_2';
-- 二年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 4, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_2';
-- 二年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 4, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_2';
-- 二年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 4, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_2';
-- 三年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 5, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_3';
-- 三年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 5, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_3';
-- 三年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 5, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_3';
-- 三年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 6, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_3';
-- 三年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 6, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_3';
-- 三年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 6, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_3';
-- 四年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 7, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_4';
-- 四年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 7, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_4';
-- 四年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 7, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_4';
-- 四年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 8, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_4';
-- 四年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 8, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_4';
-- 四年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 8, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_4';
-- 五年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 9, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_5';
-- 五年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 9, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_5';
-- 五年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 9, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_5';
-- 五年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 10, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_5';
-- 五年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 10, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_5';
-- 五年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 10, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_5';
-- 六年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 11, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_6';
-- 六年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 11, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_6';
-- 六年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 11, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_6';
-- 六年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 12, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_6';
-- 六年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 12, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_6';
-- 六年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 12, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_6';
```

### 初中

```sql
-- 七年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期中 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 13, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 七年级期末 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 14, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_7';
-- 八年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期中 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 15, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 八年级期末 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 16, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_8';
-- 九年级期中 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期中 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 17, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
-- 九年级期末 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 18, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'GRADE_9';
```

### 高中

```sql
-- 高一模拟考 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 生物
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 6,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一模拟考 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 19, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 生物
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 6,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高一月考 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 20, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_1';
-- 高二模拟考 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 生物
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 6,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二模拟考 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 21, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 生物
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 6,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高二月考 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 22, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_2';
-- 高三模拟考 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 生物
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 6,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三模拟考 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 23, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 语文
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 1,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 数学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 2,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 英语
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 3,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 物理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 4,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 化学
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 5,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 生物
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 6,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 政治
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 7,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 历史
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 8,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 地理
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 9,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
-- 高三月考 · 体育
INSERT INTO score (student_id, exam_id, subject_id, score)
SELECT sp.id, 24, 13,
       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)
FROM student_profile sp
JOIN dict_class dc ON sp.class_id_id = dc.id
WHERE dc.grade = 'SENIOR_3';
```

---

## 三、数据量统计

| 学段 | 年级数 | 考试数 | 每场科目 | 每级学生 | 成绩总数 |
|------|--------|--------|----------|----------|----------|
| 小学 | 6 | 12 | 3 | ~300 | 10,800 |
| 初中 | 3 | 6 | 9 | ~240 | 12,960 |
| 高中 | 3 | 6 | 10 | ~180 | 10,800 |
| **合计** | **12** | **24** | — | — | **34,560** |

### 按年级明细

| 年级 | 学生数 | 考试类型 | 科目数 | 成绩条数 |
|------|--------|----------|--------|----------|
| 一年级 | 300 | 期中、期末 | 3 | 1,800 |
| 二年级 | 300 | 期中、期末 | 3 | 1,800 |
| 三年级 | 300 | 期中、期末 | 3 | 1,800 |
| 四年级 | 300 | 期中、期末 | 3 | 1,800 |
| 五年级 | 300 | 期中、期末 | 3 | 1,800 |
| 六年级 | 300 | 期中、期末 | 3 | 1,800 |
| 七年级 | 240 | 期中、期末 | 9 | 4,320 |
| 八年级 | 240 | 期中、期末 | 9 | 4,320 |
| 九年级 | 240 | 期中、期末 | 9 | 4,320 |
| 高一 | 180 | 模拟考、月考 | 10 | 3,600 |
| 高二 | 180 | 模拟考、月考 | 10 | 3,600 |
| 高三 | 180 | 模拟考、月考 | 10 | 3,600 |

---

## 使用说明

1. **备份数据库**：`cp db.sqlite3 db.sqlite3.bak`  

2. **执行 SQL**：在 SQLite 命令行或 DB Browser 中打开本文件执行  

3. **验证**：`python manage.py check` 确认无误  

4. **清空重来**（如需）：`DELETE FROM score; DELETE FROM exam_plan;` 后再执行  
