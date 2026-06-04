from django.db import migrations


def seed_research_groups(apps, schema_editor):
    ResearchGroupDict = apps.get_model('dicts', 'ResearchGroupDict')
    ResearchGroupDict.objects.bulk_create([
        ResearchGroupDict(name=name) for name in [
            '语文组', '数学组', '英语组', '物理组',
            '化学组', '地理组', '生物组', '体育组',
        ]
    ], ignore_conflicts=True)


def reverse_seed(apps, schema_editor):
    ResearchGroupDict = apps.get_model('dicts', 'ResearchGroupDict')
    ResearchGroupDict.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('dicts', '0004_seed_classes'),
    ]

    operations = [
        migrations.RunPython(seed_research_groups, reverse_seed),
    ]
