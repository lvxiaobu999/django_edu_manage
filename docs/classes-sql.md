# SQL 操作语法记录

## 项目数据库操作

```bash
# 进入 SQLite 命令行
uv run python manage.py dbshell

# 直接执行 SQL 文件
uv run python manage.py dbshell < docs/class_data.sql
```

## 生成所有班级数据

规则：
- 小学（一年级 ~ 六年级）：每个年级 10 个班
- 初中（七年级 ~ 九年级）：每个年级 8 个班
- 高中（高一 ~ 高三）：每个年级 6 个班

合计：6×10 + 3×8 + 3×6 = 102 个班级

```sql
-- ====== 小学 ======
-- 一年级
INSERT INTO classes (grade, name) VALUES
('GRADE_1', '1班'), ('GRADE_1', '2班'), ('GRADE_1', '3班'), ('GRADE_1', '4班'), ('GRADE_1', '5班'),
('GRADE_1', '6班'), ('GRADE_1', '7班'), ('GRADE_1', '8班'), ('GRADE_1', '9班'), ('GRADE_1', '10班');

-- 二年级
INSERT INTO classes (grade, name) VALUES
('GRADE_2', '1班'), ('GRADE_2', '2班'), ('GRADE_2', '3班'), ('GRADE_2', '4班'), ('GRADE_2', '5班'),
('GRADE_2', '6班'), ('GRADE_2', '7班'), ('GRADE_2', '8班'), ('GRADE_2', '9班'), ('GRADE_2', '10班');

-- 三年级
INSERT INTO classes (grade, name) VALUES
('GRADE_3', '1班'), ('GRADE_3', '2班'), ('GRADE_3', '3班'), ('GRADE_3', '4班'), ('GRADE_3', '5班'),
('GRADE_3', '6班'), ('GRADE_3', '7班'), ('GRADE_3', '8班'), ('GRADE_3', '9班'), ('GRADE_3', '10班');

-- 四年级
INSERT INTO classes (grade, name) VALUES
('GRADE_4', '1班'), ('GRADE_4', '2班'), ('GRADE_4', '3班'), ('GRADE_4', '4班'), ('GRADE_4', '5班'),
('GRADE_4', '6班'), ('GRADE_4', '7班'), ('GRADE_4', '8班'), ('GRADE_4', '9班'), ('GRADE_4', '10班');

-- 五年级
INSERT INTO classes (grade, name) VALUES
('GRADE_5', '1班'), ('GRADE_5', '2班'), ('GRADE_5', '3班'), ('GRADE_5', '4班'), ('GRADE_5', '5班'),
('GRADE_5', '6班'), ('GRADE_5', '7班'), ('GRADE_5', '8班'), ('GRADE_5', '9班'), ('GRADE_5', '10班');

-- 六年级
INSERT INTO classes (grade, name) VALUES
('GRADE_6', '1班'), ('GRADE_6', '2班'), ('GRADE_6', '3班'), ('GRADE_6', '4班'), ('GRADE_6', '5班'),
('GRADE_6', '6班'), ('GRADE_6', '7班'), ('GRADE_6', '8班'), ('GRADE_6', '9班'), ('GRADE_6', '10班');

-- ====== 初中 ======
-- 七年级
INSERT INTO classes (grade, name) VALUES
('GRADE_7', '1班'), ('GRADE_7', '2班'), ('GRADE_7', '3班'), ('GRADE_7', '4班'),
('GRADE_7', '5班'), ('GRADE_7', '6班'), ('GRADE_7', '7班'), ('GRADE_7', '8班');

-- 八年级
INSERT INTO classes (grade, name) VALUES
('GRADE_8', '1班'), ('GRADE_8', '2班'), ('GRADE_8', '3班'), ('GRADE_8', '4班'),
('GRADE_8', '5班'), ('GRADE_8', '6班'), ('GRADE_8', '7班'), ('GRADE_8', '8班');

-- 九年级
INSERT INTO classes (grade, name) VALUES
('GRADE_9', '1班'), ('GRADE_9', '2班'), ('GRADE_9', '3班'), ('GRADE_9', '4班'),
('GRADE_9', '5班'), ('GRADE_9', '6班'), ('GRADE_9', '7班'), ('GRADE_9', '8班');

-- ====== 高中 ======
-- 高一
INSERT INTO classes (grade, name) VALUES
('SENIOR_1', '1班'), ('SENIOR_1', '2班'), ('SENIOR_1', '3班'),
('SENIOR_1', '4班'), ('SENIOR_1', '5班'), ('SENIOR_1', '6班');

-- 高二
INSERT INTO classes (grade, name) VALUES
('SENIOR_2', '1班'), ('SENIOR_2', '2班'), ('SENIOR_2', '3班'),
('SENIOR_2', '4班'), ('SENIOR_2', '5班'), ('SENIOR_2', '6班');

-- 高三
INSERT INTO classes (grade, name) VALUES
('SENIOR_3', '1班'), ('SENIOR_3', '2班'), ('SENIOR_3', '3班'),
('SENIOR_3', '4班'), ('SENIOR_3', '5班'), ('SENIOR_3', '6班');
```

## grade 枚举对照

| 数据库值 | 中文名 | 学段 |
|----------|--------|------|
| `GRADE_1` | 一年级 | 小学 |
| `GRADE_2` | 二年级 | 小学 |
| `GRADE_3` | 三年级 | 小学 |
| `GRADE_4` | 四年级 | 小学 |
| `GRADE_5` | 五年级 | 小学 |
| `GRADE_6` | 六年级 | 小学 |
| `GRADE_7` | 七年级 | 初中 |
| `GRADE_8` | 八年级 | 初中 |
| `GRADE_9` | 九年级 | 初中 |
| `SENIOR_1` | 高一 | 高中 |
| `SENIOR_2` | 高二 | 高中 |
| `SENIOR_3` | 高三 | 高中 |

## 验证

```sql
-- 查看各年级班级数量
SELECT grade, COUNT(*) AS cnt FROM classes GROUP BY grade ORDER BY grade;

-- 查看所有班级
SELECT grade, name FROM classes ORDER BY grade, name;
```
