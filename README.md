# VGoru — Веб-платформа гірських маршрутів

Каталог туристичних маршрутів Українських Карпат на базі Django. Платформа дозволяє шукати маршрути, вести облік пройдених шляхів та залишати відгуки.

## Функціональність

- Каталог маршрутів з фільтрацією за регіоном, складністю та висотою
- Сторінка кожного маршруту з картою Leaflet та відгуками
- Реєстрація, вхід, профіль користувача
- Додавання маршрутів до улюблених та відмітка пройдених
- Система відгуків з рейтингом
- Панель адміністратора

## Технічний стек

- Python 3.10+, Django 5.2, SQLite
- Leaflet для інтерактивних карт
- Pillow для обробки зображень
- Модульний CSS з повноцінною системою дизайн-токенів

## Встановлення

```bash
git clone <URL>
cd vgoru

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Опціонально: тестові дані (15 маршрутів, 8 користувачів, ~40 відгуків)
python load_test_data.py

python manage.py runserver
```

Застосунок: http://127.0.0.1:8000  
Адмін-панель: http://127.0.0.1:8000/admin

## Структура проекту

```
vgoru/
├── manage.py
├── load_test_data.py
├── requirements.txt
├── vgoru/                          # Конфігурація проекту
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── settings/
│       ├── base.py                 # Спільні налаштування
│       └── local.py                # Локальна розробка (DEBUG, DB)
└── mountains_roads/                # Основний додаток
    ├── models.py
    ├── forms.py
    ├── mixins.py                   # AuthorRequiredMixin, CssWidgetMixin тощо
    ├── signals.py                  # Авто-створення профілю, оновлення рейтингу
    ├── admin.py
    ├── apps.py
    ├── views/
    │   ├── routes.py               # HomePageView, RoutesListView, RouteDetailView
    │   ├── reviews.py              # ReviewCreateView, Update, Delete
    │   ├── users.py                # UserProfileView, Registration, Update
    │   └── ajax.py                 # toggle_favorite, toggle_completed
    ├── urls/
    │   ├── routes.py
    │   ├── reviews.py
    │   └── users.py
    ├── templates/mountains_roads/
    │   ├── base.html
    │   ├── partials/               # route_card.html, star_rating.html
    │   └── *.html
    └── static/mountains_roads/
        ├── css/
        │   ├── styles.css          # Точка входу — імпортує всі модулі
        │   ├── base/               # variables.css, reset.css, layout.css
        │   ├── components/         # navbar, buttons, cards, forms, alerts, footer
        │   └── pages/              # home, routes, user, reviews
        └── js/
            └── scripts.js
```

## Змінні середовища

| Змінна               | За замовчуванням          | Опис                       |
|----------------------|---------------------------|----------------------------|
| `DJANGO_SETTINGS_MODULE` | `vgoru.settings.local` | Модуль налаштувань     |
| `DJANGO_SECRET_KEY`  | (insecure dev key)        | Секретний ключ Django       |

Для продакшену створіть `vgoru/settings/production.py` на основі `base.py` з `DEBUG=False` та змінними середовища.
