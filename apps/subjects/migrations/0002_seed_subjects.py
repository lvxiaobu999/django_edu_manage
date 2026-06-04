from django.db import migrations


def seed_subjects(apps, schema_editor):
    Subjects = apps.get_model('subjects', 'Subjects')
    Subjects.objects.bulk_create([
        Subjects(name=name) for name in [
            # 小学 / 初中 / 高中共同科目
            '语文',
            '数学',
            '英语',
            # 初中 / 高中
            '物理',
            '化学',
            '生物',
            '地理',
            '历史',
            # 政治类（各学段叫法不同，取"政治"为统称）
            '政治',
            # 小学科学
            '科学',
            # 体育与健康
            '体育',
            # 艺术类
            '音乐',
            '美术',
            # 信息技术
            '信息技术',
            # 高中通用技术
            '通用技术',
            # 劳动教育
            '劳动',
            # 综合实践活动
            '综合实践',
            # 书法（小学）
            '书法',
            # 心理健康教育
            '心理健康',
        ]
    ], ignore_conflicts=True)


def reverse_seed(apps, schema_editor):
    Subjects = apps.get_model('subjects', 'Subjects')
    Subjects.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_subjects, reverse_seed),
    ]
