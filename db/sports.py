from db.models import Sport


base_sports = [
    "Авиамодельный спорт",
    "Автомобильный спорт",
    "Айкидо",
    "Акробатический рок-н-ролл",
    "Альпинизм",
    "Американский футбол",
    "Армреслинг",
    "Бадминтон",
    "Баскетбол",
    "Бейсбол",
    "Биатлон",
    "Бильярдный спорт",
    "Бобслей",
    "Бодибилдинг",
    "Бокс",
    "Борьба на поясах",
    "Боулинг",
    "Велосипедный спорт",
    "Вертолетный спорт",
    "Водно-моторный спорт",
    "Водное поло",
    "Воднолыжный спорт",
    "Воздухоплавательный спорт",
    "Воздушно-силовая атлетика (воркаут)",
    "Волейбол",
    "Восточное боевое единоборство",
    "Всестилевое каратэ",
    "Гандбол",
    "Гиревой спорт",
    "Го",
    "Гольф",
    "Гонки с препятствиями",
    "Горнолыжный спорт",
    "Городошный спорт",
    "Гребля на байдарках и каноэ",
    "Гребля слалом",
    "Гребной спорт",
    "Дартс",
    "Джиу-джитсу",
    "Дзюдо",
    "Ездовой спорт",
    "Каратэ",
    "Кендо",
    "Керлинг",
    "Кикбоксинг",
    "Кинологический спорт",
    "Киокусинкай",
    "Киокушин",
    "Компьютерный спорт",
    "Конный спорт",
    "Конькобежный спорт",
    "Кореш",
    "Кудо",
    "Лапта",
    "Легкая атлетика",
    "Лыжное двоеборье",
    "Лыжные гонки",
    "Морское многоборье",
    "Мотоциклетный спорт",
    "Муатай",
    "Настольный теннис",
    "Парашютный спорт",
    "Парусный спорт",
    "Пауэрлифтинг",
    "Перетягивание каната",
    "Плавание",
    "Планерный спорт",
    "Подводный спорт",
    "Полиатлон",
    "Практическая стрельба",
    "Прыжки в воду",
    "Прыжки на батуте",
    "Прыжки на лыжах с трамплина",
    "Пулевая стрельба",
    "Пэйнтбол",
    "Радиоспорт",
    "Рафтинг",
    "Регби",
    "Роллер спорт",
    "Роуп скиппинг (спортивная скакалка)",
    "Рукопашный бой",
    "Рыболовный спорт",
    "Сават",
    "Самбо",
    "Самолетный спорт",
    "Санный спорт",
    "Северное многоборье",
    "Серфинг",
    "Синхронное плавание",
    "Скалолазание",
    "Сквош",
    "Скейтбординг",
    "Смешанное боевое единоборство (ММА)",
    "Сноуборд",
    "Современное пятиборье",
    "Софтбол",
    "Спорт сверхлегкой авиации",
    "Спортивно-прикладное собаководство",
    "Спортивное метание ножа",
    "Спортивная борьба",
    "Спорт глухих",
    "Спорт лиц с интеллектуальными нарушениями",
    "Спорт лиц с поражением ОДА",
    "Спорт слепых",
    "Спортивная акробатика",
    "Спортивная аэробика",
    "Спортивная гимнастика",
    "Спортивное ориентирование",
    "Спортивное программирование",
    "Спортивный туризм",
    "Стендовая стрельба",
    "Страйкбол",
    "Стрельба из арбалета",
    "Стрельба из лука",
    "Судомодельный спорт",
    "Сумо",
    "Танцевальный спорт",
    "Теннис",
    "Триатлон",
    "Тхэквондо",
    "Тяжелая атлетика",
    "Универсальный бой",
    "Ушу",
    "Фехтование",
    "Фигурное катание на коньках",
    "Фитнес-аэробика",
    "Флорбол",
    "Фристайл",
    "Функциональное многоборье",
    "Футбол",
    "Футбол лиц с заболеванием ЦП",
    "Хоккей",
    "Хоккей на траве",
    "Хоккей с мячом",
    "Художественная гимнастика",
    "Чир спорт",
    "Шахматы",
    "Шашки",
    "Эстетическая гимнастика",
    "Керешу",
    "Мас-рестлинг",
    "Таврели",
    "Хапсагай",
    "Хуреш",
    "Шодсанлат",
    "Якутские национальные прыжки",
]


def base_populate_sport_table(app, db):
    with app.app_context():
        for sport_name in base_sports:
            sport = Sport(name=sport_name)
            # Insert sport uniquely
            exists = Sport.query.filter_by(name=sport_name).first()
            if not exists:
                db.session.add(sport)
        db.session.commit()
        print(f"Inserted base entries in sport table.")
