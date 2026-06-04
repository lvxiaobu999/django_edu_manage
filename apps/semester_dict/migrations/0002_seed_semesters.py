from django.db import migrations


def seed_semesters(apps, schema_editor):
    Semester = apps.get_model('semester_dict', 'Semester')
    years = ['2023-2024', '2024-2025', '2025-2026', '2026-2027']
    Semester.objects.bulk_create([
        Semester(name=f'{y}-1', display_name=f'{y}学年第一学期') for y in years
    ] + [
        Semester(name=f'{y}-2', display_name=f'{y}学年第二学期') for y in years
    ], ignore_conflicts=True)


def reverse_seed(apps, schema_editor):
    Semester = apps.get_model('semester_dict', 'Semester')
    Semester.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('semester_dict', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_semesters, reverse_seed),
    ]
