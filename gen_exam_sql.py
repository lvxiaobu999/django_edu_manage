"""生成 exam-sql.md。运行：python gen_exam_sql.py > exam-sql.md"""

SUBJECTS = {
    '语文': 1, '数学': 2, '英语': 3, '物理': 4, '化学': 5,
    '生物': 6, '政治': 7, '历史': 8, '地理': 9, '体育': 13,
}
SEMESTER_ID = 3  # 2025-2026学年第一学期

GRADE_LABEL = {
    'GRADE_1': '一年级', 'GRADE_2': '二年级', 'GRADE_3': '三年级',
    'GRADE_4': '四年级', 'GRADE_5': '五年级', 'GRADE_6': '六年级',
    'GRADE_7': '七年级', 'GRADE_8': '八年级', 'GRADE_9': '九年级',
    'SENIOR_1': '高一', 'SENIOR_2': '高二', 'SENIOR_3': '高三',
}

STUDENT_COUNT = {
    'GRADE_1': 300, 'GRADE_2': 300, 'GRADE_3': 300,
    'GRADE_4': 300, 'GRADE_5': 300, 'GRADE_6': 300,
    'GRADE_7': 240, 'GRADE_8': 240, 'GRADE_9': 240,
    'SENIOR_1': 180, 'SENIOR_2': 180, 'SENIOR_3': 180,
}

# ── 考试计划定义 ──
# (学段标签, 年级列表, 考试类型列表, 科目列表, 日期起始偏移)
PLAN = [
    ('小学', ['GRADE_1','GRADE_2','GRADE_3','GRADE_4','GRADE_5','GRADE_6'],
     [('MIDTERM','期中','2025-11-{:02d}'), ('FINAL','期末','2026-01-{:02d}')],
     ['语文','数学','英语'], 0),

    ('初中', ['GRADE_7','GRADE_8','GRADE_9'],
     [('MIDTERM','期中','2025-11-{:02d}'), ('FINAL','期末','2026-01-{:02d}')],
     ['语文','数学','英语','物理','化学','政治','历史','地理','体育'], 10),

    ('高中', ['SENIOR_1','SENIOR_2','SENIOR_3'],
     [('MOCK','模拟考','2025-10-{:02d}'), ('MONTHLY','月考','2025-12-{:02d}')],
     ['语文','数学','英语','物理','化学','生物','政治','历史','地理','体育'], 20),
]


def gen_exam_plan_name(semester, grade_label, exam_label):
    if exam_label.endswith('考'):
        return f'{semester}{grade_label}{exam_label}试'
    return f'{semester}{grade_label}{exam_label}考试'


def main():
    exam_id = 0
    exam_list = []  # [(id, grade, grade_label, type_label, name, date, subjects, section)]

    # 构建考试计划
    for section, grades, exam_types, subjects, date_off in PLAN:
        for gi, grade in enumerate(grades):
            for etype, elabel, date_fmt in exam_types:
                exam_id += 1
                day = date_off + gi + 1
                date = date_fmt.format(day)
                name = gen_exam_plan_name('2025-2026学年第一学期', GRADE_LABEL[grade], elabel)
                exam_list.append({
                    'id': exam_id, 'grade': grade, 'grade_label': GRADE_LABEL[grade],
                    'type': etype, 'type_label': elabel,
                    'name': name, 'date': date, 'subjects': subjects, 'section': section,
                })

    # ── 输出 Markdown ──
    out = []
    out.append('# 考试模拟数据 SQL\n')
    out.append('> **学期**：2025-2026 学年第一学期（semester_id=3）  ')
    out.append('> **满分**：100 分 | **随机范围**：40.0 ~ 100.0（保留 1 位小数）  ')
    out.append('> **策略**：INSERT INTO ... SELECT 批量生成，避免逐行 VALUES。\n')
    out.append('## 目录\n')
    out.append('1. [考试计划](#一考试计划-exam_plan)  ')
    out.append('2. [成绩数据](#二成绩数据-score)  ')
    out.append('3. [数据量统计](#三数据量统计)\n')
    out.append('---\n')

    # ── 一、考试计划 ──
    out.append('## 一、考试计划（exam_plan）\n')
    out.append('```sql')

    for ep in exam_list:
        out.append(
            f"INSERT INTO exam_plan (id, name, exam_type, exam_date, grade, semester_id)"
            f" VALUES ({ep['id']}, '{ep['name']}', '{ep['type']}', "
            f"'{ep['date']}', '{ep['grade']}', {SEMESTER_ID});"
        )
    out.append('```\n')

    # 汇总表
    out.append('| 学段 | 年级 | 考试类型 | 日期 | 科目 |')
    out.append('|------|------|----------|------|------|')
    for ep in exam_list:
        out.append(f"| {ep['section']} | {ep['grade_label']} | {ep['type_label']} "
                   f"| {ep['date']} | {'、'.join(ep['subjects'])} |")
    out.append('')

    # ── 二、成绩 ──
    out.append('---\n')
    out.append('## 二、成绩数据（score）\n')

    total_scores = 0
    for section, _, _, _, _ in PLAN:
        sec_exams = [e for e in exam_list if e['section'] == section]
        out.append(f'### {section}\n')
        out.append('```sql')

        sec_scores = 0
        for ep in sec_exams:
            for subj in ep['subjects']:
                sid = SUBJECTS[subj]
                stu_n = STUDENT_COUNT[ep['grade']]
                sec_scores += stu_n
                out.append(
                    f"-- {ep['grade_label']}{ep['type_label']} · {subj}"
                )
                # RANDOM(): (ABS(RANDOM())%601+400)/10.0 = 40.0~100.0
                out.append(
                    f"INSERT INTO score (student_id, exam_id, subject_id, score)\n"
                    f"SELECT sp.id, {ep['id']}, {sid},\n"
                    f"       CAST((ABS(RANDOM()) % 601 + 400) / 10.0 AS REAL)\n"
                    f"FROM student_profile sp\n"
                    f"JOIN dict_class dc ON sp.class_id_id = dc.id\n"
                    f"WHERE dc.grade = '{ep['grade']}';"
                )

        total_scores += sec_scores
        out.append('```\n')

    # ── 三、数据量统计 ──
    out.append('---\n')
    out.append('## 三、数据量统计\n')
    out.append('| 学段 | 年级数 | 考试数 | 每场科目 | 每级学生 | 成绩总数 |')
    out.append('|------|--------|--------|----------|----------|----------|')
    for section, grades, exam_types, subjects, _ in PLAN:
        n_grades = len(grades)
        n_exams = n_grades * len(exam_types)
        n_subjects = len(subjects)
        avg_stu = sum(STUDENT_COUNT[g] for g in grades) // n_grades

        sec_total = 0
        for g in grades:
            sec_total += STUDENT_COUNT[g] * len(exam_types) * len(subjects)

        out.append(f'| {section} | {n_grades} | {n_exams} | {n_subjects} | ~{avg_stu} | {sec_total:,} |')

    out.append(f'| **合计** | **12** | **24** | — | — | **{total_scores:,}** |')
    out.append('')

    # 按年级明细
    out.append('### 按年级明细\n')
    out.append('| 年级 | 学生数 | 考试类型 | 科目数 | 成绩条数 |')
    out.append('|------|--------|----------|--------|----------|')
    for section, grades, exam_types, subjects, _ in PLAN:
        for g in grades:
            grade_exams = [e for e in exam_list if e['grade'] == g]
            n = STUDENT_COUNT[g] * len(grade_exams) * len(subjects)
            exam_labels = '、'.join(e['type_label'] for e in grade_exams)
            out.append(f"| {GRADE_LABEL[g]} | {STUDENT_COUNT[g]} | {exam_labels} | {len(subjects)} | {n:,} |")
    out.append('')

    # 使用说明
    out.append('---\n')
    out.append('## 使用说明\n')
    out.append('1. **备份数据库**：`cp db.sqlite3 db.sqlite3.bak`  \n')
    out.append('2. **执行 SQL**：在 SQLite 命令行或 DB Browser 中打开本文件执行  \n')
    out.append('3. **验证**：`python manage.py check` 确认无误  \n')
    out.append('4. **清空重来**（如需）：`DELETE FROM score; DELETE FROM exam_plan;` 后再执行  \n')

    return '\n'.join(out)


if __name__ == '__main__':
    import sys
    output_path = sys.argv[1] if len(sys.argv) > 1 else './docs/exam-sql.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(main())
    print(f'Written to {output_path}')
