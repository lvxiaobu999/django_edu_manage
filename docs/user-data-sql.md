# 教师学生测试数据

## 数据概览

| 角色 | 数量 | 说明 |
|------|------|------|
| 教师 | 120 | 已激活，已分配教研组和所教班级 |
| 学生 | 3,060 | 每班 30 人，102 个班全覆盖 |
| 班级 | 102 | 全部已指定班主任 |
| 教研组 | 8 | 每组 15-33 位教师 |

性别分布：教师约 66% 男 / 34% 女；学生约 50% / 50%。

## 登录账号

所有账号密码统一为：**`password123`**

### 教师账号

```
用户名格式：teacher001 ~ teacher120
示例：teacher001 / password123
```

### 学生账号

```
用户名格式：student0001 ~ student3060
示例：student0001 / password123
```

## 数据关系

```
教师 TeacherProfile
  ├── user         → User (role=TEACHER)
  ├── research_groups → ResearchGroup (1~2个教研组)
  ├── class_ids      → Classes (1~4个所教班级)
  └── 102个班级的 headmaster 由前102位教师担任

学生 StudentProfile
  ├── user     → User (role=STUDENT)
  └── class_id → Classes (每班30人)
```

## 验证 SQL

```sql
-- 各年级学生人数
SELECT SUBSTR(c.grade, 1, 7) AS 年级, COUNT(sp.id) AS 学生数
FROM classes c
LEFT JOIN student_profile sp ON sp.class_id_id = c.id
GROUP BY c.grade
ORDER BY c.grade;

-- 各教研组教师人数
SELECT rg.name AS 教研组, COUNT(tprg.teacherprofile_id) AS 教师数
FROM research_group rg
LEFT JOIN teacher_profile_research_groups tprg ON rg.id = tprg.researchgroup_id
GROUP BY rg.id, rg.name
ORDER BY rg.id;

-- 各班学生人数
SELECT c.grade || c.name AS 班级, COUNT(sp.id) AS 学生数
FROM classes c
LEFT JOIN student_profile sp ON sp.class_id_id = c.id
GROUP BY c.id
ORDER BY c.grade, c.name;

-- 查看某教师所教班级
SELECT tp.realname, c.grade || c.name AS 班级
FROM teacher_profile tp
JOIN teacher_profile_class_ids tpci ON tp.id = tpci.teacherprofile_id
JOIN classes c ON c.id = tpci.classes_id
WHERE tp.emp_no = 'T2026001';
```
