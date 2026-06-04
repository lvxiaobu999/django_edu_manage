from django.db import migrations


def seed_dicts(apps, schema_editor):
    SubjectDict = apps.get_model('dicts', 'SubjectDict')
    SemesterDict = apps.get_model('dicts', 'SemesterDict')

    # 科目种子数据（中小学全科）
    SubjectDict.objects.bulk_create([
        SubjectDict(name=name) for name in [
            '语文', '数学', '英语', '物理', '化学', '生物',
            '地理', '历史', '政治', '科学', '体育', '音乐',
            '美术', '信息技术', '通用技术', '劳动', '综合实践',
            '书法', '心理健康',
        ]
    ], ignore_conflicts=True)

    # 学期种子数据（2023 ~ 2027 四个学年）
    years = ['2023-2024', '2024-2025', '2025-2026', '2026-2027']
    SemesterDict.objects.bulk_create([
        SemesterDict(name=f'{y}-1', display_name=f'{y}学年第一学期') for y in years
    ] + [
        SemesterDict(name=f'{y}-2', display_name=f'{y}学年第二学期') for y in years
    ], ignore_conflicts=True)


def reverse_seed(apps, schema_editor):
    SubjectDict = apps.get_model('dicts', 'SubjectDict')
    SemesterDict = apps.get_model('dicts', 'SemesterDict')
    SubjectDict.objects.all().delete()
    SemesterDict.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('dicts', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(seed_dicts, reverse_seed),
    ]
