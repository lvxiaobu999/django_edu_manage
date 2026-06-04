import hashlib

from django.contrib.auth.hashers import make_password
from django.db import migrations

# === 姓名生成数据 ===
SURNAMES = [
    '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
    '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
    '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏',
    '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
    '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦',
    '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
    '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪',
    '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐',
    '于', '时', '傅', '皮', '齐', '康', '伍', '余', '元', '卜',
    '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵',
]

MALE_CHARS = [
    '伟', '强', '勇', '军', '志', '峰', '建', '国', '文', '杰',
    '明', '辉', '斌', '涛', '鹏', '飞', '宇', '浩', '海', '健',
    '磊', '超', '波', '亮', '刚', '华', '林', '平', '章', '龙',
    '翔', '毅', '俊', '云', '帆', '博', '睿', '凯', '旭', '晨',
    '宁', '远', '哲', '恒', '思', '正', '安', '威', '豪', '诚',
]

FEMALE_CHARS = [
    '芳', '敏', '静', '丽', '娟', '秀', '英', '娜', '婷', '雪',
    '梅', '兰', '花', '玲', '玉', '红', '春', '燕', '洁', '文',
    '芬', '霞', '蕾', '云', '欣', '萍', '慧', '莉', '怡', '萌',
    '瑶', '佳', '婉', '琴', '月', '君', '颖', '悦', '诗', '雅',
    '晓', '雨', '岚', '露', '萱', '若', '冰', '柔', '艺', '仪',
]

BATCH = 500


def _hash_pick(seed, items):
    h = int(hashlib.md5(str(seed).encode()).hexdigest()[:8], 16)
    return items[h % len(items)]


def _realname(idx, gender):
    s = _hash_pick(f's_{idx}', SURNAMES)
    pool = MALE_CHARS if gender == 'MALE' else FEMALE_CHARS
    c1 = _hash_pick(f'c1_{idx}', pool)
    c2 = _hash_pick(f'c2_{idx}', pool)
    return s + c1 + c2


def _gender(idx, total, male_ratio):
    male_count = int(total * male_ratio)
    return 'MALE' if idx <= male_count else 'FEMALE'


def seed_users_profiles(apps, schema_editor):
    User = apps.get_model('users', 'User')
    TeacherProfile = apps.get_model('user_profile', 'TeacherProfile')
    StudentProfile = apps.get_model('user_profile', 'StudentProfile')
    ClassDict = apps.get_model('dicts', 'ClassDict')
    ResearchGroupDict = apps.get_model('dicts', 'ResearchGroupDict')

    pw_hash = make_password('z123456.')

    # 直接用 pk 列表查询，不用 order_by（避免 migration state 不包含字段的罕见兼容问题）
    class_ids = list(
        ClassDict.objects.values_list('id', flat=True).order_by('grade', 'name')
    )
    group_ids = list(
        ResearchGroupDict.objects.values_list('id', flat=True).order_by('id')
    )

    if len(class_ids) != 102 or len(group_ids) != 8:
        raise RuntimeError(
            f'Expected 102 classes and 8 research groups, '
            f'got {len(class_ids)} and {len(group_ids)}. '
            f'Run "migrate dicts" first.'
        )

    # 从 DB 获取真实实例（M2M add 需要 db 状态，裸实例不行）
    classes_all = list(
        ClassDict.objects.filter(id__in=class_ids).order_by('grade', 'name')
    )
    groups = list(
        ResearchGroupDict.objects.filter(id__in=group_ids).order_by('id')
    )

    # ============================================================
    # 1. 创建 120 位教师 User + TeacherProfile
    # ============================================================
    teacher_users = []
    for i in range(1, 121):
        gender = _gender(i, 120, 0.66)
        teacher_users.append(User(
            username=f'teacher{i:03d}',
            password=pw_hash,
            role='TEACHER',
            is_active=True,
            is_approved=True,
            real_name=_realname(i, gender),
        ))

    User.objects.bulk_create(teacher_users)

    teacher_user_objs = list(
        User.objects.filter(role='TEACHER').order_by('username')
    )

    teacher_profiles = []
    for idx, user in enumerate(teacher_user_objs):
        i = idx + 1
        gender = _gender(i, 120, 0.66)
        teacher_profiles.append(TeacherProfile(
            user=user,
            emp_no=f'T2026{i:03d}',
            realname=user.real_name,
            gender=gender,
            age=25 + (i % 20),
            phone=f'138{10000000 + i:08d}'[:11],
            email=f'teacher{i:03d}@school.edu.cn',
            address=f'教师宿舍{i % 10 + 1}号楼{i:03d}室',
        ))

    TeacherProfile.objects.bulk_create(teacher_profiles)

    teacher_profiles_db = list(
        TeacherProfile.objects.order_by('emp_no')
    )

    # 教研组分配：8 组 × 各 15 人
    for idx, teacher in enumerate(teacher_profiles_db):
        teacher.research_groups.add(groups[idx % len(groups)])

    # 所教班级分配：每个老师 1-4 个班
    for idx, teacher in enumerate(teacher_profiles_db):
        n_classes = (idx % 4) + 1
        start = (idx * 3) % len(classes_all)
        for j in range(n_classes):
            cls = classes_all[(start + j) % len(classes_all)]
            teacher.class_ids.add(cls)

    # 班主任分配：前 102 位老师对应 102 个班级
    for i, cls in enumerate(classes_all):
        if i < len(teacher_profiles_db):
            cls.headmaster = teacher_profiles_db[i]
            cls.save(update_fields=['headmaster'])

    # ============================================================
    # 2. 创建 3060 名学生 User + StudentProfile
    # ============================================================
    student_users = []
    for i in range(1, 3061):
        gender = _gender(i, 3060, 0.5)
        student_users.append(User(
            username=f'student{i:04d}',
            password=pw_hash,
            role='STUDENT',
            is_active=True,
            is_approved=True,
            real_name=_realname(1000 + i, gender),
        ))

    User.objects.bulk_create(student_users)

    student_user_objs = list(
        User.objects.filter(role='STUDENT').order_by('username')
    )

    student_profiles = []
    for idx, user in enumerate(student_user_objs):
        i = idx + 1
        gender = _gender(i, 3060, 0.5)
        class_idx = (i - 1) // 30
        student_profiles.append(StudentProfile(
            user=user,
            stu_no=f'S2026{i:04d}',
            realname=user.real_name,
            gender=gender,
            age=6 + class_idx // 20,
            class_id=classes_all[class_idx],
        ))

    StudentProfile.objects.bulk_create(student_profiles)


def reverse_seed(apps, schema_editor):
    User = apps.get_model('users', 'User')
    TeacherProfile = apps.get_model('user_profile', 'TeacherProfile')
    StudentProfile = apps.get_model('user_profile', 'StudentProfile')
    StudentProfile.objects.all().delete()
    TeacherProfile.objects.all().delete()
    User.objects.filter(role__in=['TEACHER', 'STUDENT']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_initial'),
    ]

    # atomic=False 避免 SQLite 事务嵌套导致 check_constraints 失败
    atomic = False

    operations = [
        migrations.RunPython(seed_users_profiles, reverse_seed),
    ]
