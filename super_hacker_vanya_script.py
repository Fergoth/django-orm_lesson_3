import random

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson

COMMENDATION_EXAMPLES = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!"
]


def get_school_kid(full_name):
    try:
        return Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.DoesNotExist:
        print("Имя не существует!")
        return None
    except Schoolkid.MultipleObjectsReturned:
        print("Несколько учеников с таким именем!")
        return None


def fix_marks(full_name):
    school_kid = get_school_kid(full_name)
    if not school_kid:
        return
    my_marks = Mark.objects.filter(schoolkid=school_kid)
    my_marks.filter(points__lte=3).update(points=5)


def remove_chastisements(full_name):
    school_kid = get_school_kid(full_name)
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=school_kid)
    schoolkid_chastisements.delete()


def create_commendation(full_name, lesson):
    school_kid = get_school_kid(full_name)
    if not school_kid:
        return
    random_lesson = Lesson.objects.filter(
        year_of_study=school_kid.year_of_study,
        group_letter=school_kid.group_letter,
        subject__title=lesson).order_by('?').first()
    if not random_lesson:
        return "Не найдено уроков с таким названием!"
    Commendation.objects.create(
        text=random.choice(COMMENDATION_EXAMPLES),
        created=random_lesson.date,
        schoolkid=school_kid,
        subject=random_lesson.subject,
        teacher=random_lesson.teacher
    )
