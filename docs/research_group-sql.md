# 教研组数据

## 数据概览

| ID | 名称 |
|----|------|
| 1 | 语文组 |
| 2 | 数学组 |
| 3 | 英语组 |
| 4 | 物理组 |
| 5 | 化学组 |
| 6 | 地理组 |
| 7 | 生物组 |
| 8 | 体育组 |

## 插入 SQL

```sql
INSERT INTO research_group (name) VALUES
('语文组'),
('数学组'),
('英语组'),
('物理组'),
('化学组'),
('地理组'),
('生物组'),
('体育组');
```

## 验证

```sql
-- 查看所有教研组
SELECT * FROM research_group ORDER BY id;

-- 查看各教研组老师数量
SELECT rg.name, COUNT(tp.id) AS teacher_count
FROM research_group rg
LEFT JOIN teacher_profile_research_groups tprg ON rg.id = tprg.researchgroup_id
LEFT JOIN teacher_profile tp ON tp.id = tprg.teacherprofile_id
GROUP BY rg.id, rg.name
ORDER BY rg.id;
```
