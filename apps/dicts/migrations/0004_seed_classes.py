from django.db import migrations


GRADE_CLASS_COUNTS = [
    ('GRADE_1', 10),
    ('GRADE_2', 10),
    ('GRADE_3', 10),
    ('GRADE_4', 10),
    ('GRADE_5', 10),
    ('GRADE_6', 10),
    ('GRADE_7', 8),
    ('GRADE_8', 8),
    ('GRADE_9', 8),
    ('SENIOR_1', 6),
    ('SENIOR_2', 6),
    ('SENIOR_3', 6),
]


def seed_classes(apps, schema_editor):
    ClassDict = apps.get_model('dicts', 'ClassDict')
    instances = []
    for grade, count in GRADE_CLASS_COUNTS:
        for i in range(1, count + 1):
            instances.append(ClassDict(grade=grade, name=f'{i}班'))
    ClassDict.objects.bulk_create(instances, ignore_conflicts=True)


def reverse_seed(apps, schema_editor):
    ClassDict = apps.get_model('dicts', 'ClassDict')
    ClassDict.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('dicts', '0003_seed_dicts'),
    ]

    operations = [
        migrations.RunPython(seed_classes, reverse_seed),
    ]
