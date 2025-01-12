from db.models import Event


base_events = [
    "Всероссийские соревнования по баскетболу среди команд общеобразовательных организаций (в рамках общероссийского проекта «Баскетбол – в школу»)",
    "Всероссийские соревнования по волейболу «Серебряный мяч» среди команд общеобразовательных организаций (в рамках общероссийского проекта «Волейбол – в школу»)",
    "Всероссийские соревнования по легкоатлетическому четырехборью «Шиповка юных» среди обучающихся общеобразовательных организаций",
    "Всероссийские соревнования по лыжным гонкам среди обучающихся общеобразовательных учреждений на призы газеты «Пионерская правда»",
    "Всероссийские соревнования по мини-футболу (футзалу) среди команд общеобразовательных организаций (в рамках общероссийского проекта «Мини-футбол – в школу»)",
    "Всероссийские соревнования юных футболистов «Кожаный мяч»",
    "Всероссийские соревнования юных хоккеистов «Золотая шайба»",
    "Открытые Всероссийские соревнования по шахматам «Белая ладья» среди команд общеобразовательных организаций",
    "Спартакиада молодежи России допризывного возраста",
    "Всероссийские спортивные соревнования школьников «Президентские состязания»",
    "Всероссийские спортивные игры школьников «Президентские спортивные игры»",
    "Всероссийские массовые соревнования по баскетболу «Оранжевый мяч»",
    "Всероссийские спортивные игры школьных спортивных клубов",
    "Открытые Всероссийские массовые соревнования по конькобежному спорту «Лед надежды нашей»",
    "Всероссийский день бега «Кросс нации»",
    "Всероссийский день ходьбы",
    "Открытая Всероссийская массовая лыжная гонка «Лыжня России»",
    "Всероссийские массовые соревнования по спортивному ориентированию «Российский Азимут»",
    "Всероссийские массовые соревнования «Оздоровительный спорт – в каждую семью»",
    "Всероссийская Спартакиада специальной олимпиады",
    "Всероссийский день самбо",
    "Всероссийская массовая велосипедная гонка",
    "Фестиваль Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО) среди обучающихся общеобразовательных организаций",
    "Фестиваль Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО) среди обучающихся образовательных организаций высшего образования",
    "Фестиваль Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО) среди семейных команд",
    "Всероссийские соревнования по многоборьям Всероссийского физкультурно-спортивного комплекса «Готов к труду и обороне» (ГТО) среди граждан, проживающих в сельской местности",
    "Всероссийская военно-патриотическая игра «Зарница»",
    "Всероссийский проект «Вызов первых»",
    "Турнир «Школьная баскетбольная лига 3х3 им. Кирилла Писклова»",
    "Турнир по волейболу среди команд общеобразовательных организаций субъектов Российской Федерации",
    "Чемпионат Школьной баскетбольной лиги «КЭС-БАСКЕТ»",
]

def base_populate_event_table(app, db):
    with app.app_context():
        for event_name in base_events:
            event = Event(name=event_name)
            # Insert event uniquely
            exists = Event.query.filter_by(name=event_name).first()
            if not exists:
                db.session.add(event)
        db.session.commit()
        print(f"Inserted base entries in event table.")
