import os
import random
import urllib.request

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vgoru.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import transaction

from mountains_roads.models import MountainRoute, RouteReview, UserProfile

USERS = [
    ('taras_shevchenko',   'Тарас',    'Шевченко'),
    ('lesya_ukrainka',     'Леся',     'Українка'),
    ('ivan_franko',        'Іван',     'Франко'),
    ('bogdan_hmel',        'Богдан',   'Хмельницький'),
    ('lina_kostenko',      'Ліна',     'Костенко'),
    ('vasyl_stus',         'Василь',   'Стус'),
    ('grigoriy_skovoroda', 'Григорій', 'Сковорода'),
    ('marusya_churay',     'Маруся',   'Чурай'),
]

ROUTES = [
    {
        'name': 'Говерла',
        'region': 'Івано-Франківська обл.',
        'height': 2061,
        'difficulty': 'medium',
        'duration': 6.0,
        'distance': 14.5,
        'description': (
            "Найвища точка України. Маршрут з бази «Заросляк». "
            "Популярний, але кам'янистий підйом."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Hoverla_View.jpg/800px-Hoverla_View.jpg',
        'coordinates': '48.1614, 24.5003',
    },
    {
        'name': 'Озеро Синевир',
        'region': 'Закарпатська обл.',
        'height': 989,
        'difficulty': 'easy',
        'duration': 2.5,
        'distance': 4.0,
        'description': (
            "Найбільше гірське озеро України, «Морське Око» Карпат. "
            "Легка прогулянка навколо озера серед смерек."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Synevir_lake_from_above.jpg/800px-Synevir_lake_from_above.jpg',
        'coordinates': '48.6163, 23.6786',
    },
    {
        'name': 'Піп Іван Чорногірський',
        'region': 'Івано-Франківська обл.',
        'height': 2028,
        'difficulty': 'hard',
        'duration': 9.0,
        'distance': 22.0,
        'description': (
            "Сходження до обсерваторії «Білий Слон». "
            "Один з наймальовничіших та найважчих маршрутів Чорногори."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Pip_Ivan_Chornohora_observatory.jpg/800px-Pip_Ivan_Chornohora_observatory.jpg',
        'coordinates': '48.0558, 24.6227',
    },
    {
        'name': 'Скелі Довбуша',
        'region': 'Івано-Франківська обл.',
        'height': 668,
        'difficulty': 'easy',
        'duration': 3.0,
        'distance': 5.0,
        'description': (
            "Унікальний скельний комплекс у буковому лісі. "
            "Місце сили та легенд про опришків."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Dovbush_rocks_2.jpg/800px-Dovbush_rocks_2.jpg',
        'coordinates': '48.8523, 24.0741',
    },
    {
        'name': 'Петрос',
        'region': 'Закарпатська обл.',
        'height': 2020,
        'difficulty': 'hard',
        'duration': 8.0,
        'distance': 16.0,
        'description': (
            "Дуже стрімкий підйом та спуск. "
            "Чудова панорама на Говерлу. Небезпечний у погану погоду."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Petros_mountain.jpg/800px-Petros_mountain.jpg',
        'coordinates': '48.1497, 24.4586',
    },
    {
        'name': 'Гимба та водоспад Шипіт',
        'region': 'Закарпатська обл.',
        'height': 1491,
        'difficulty': 'medium',
        'duration': 5.0,
        'distance': 10.0,
        'description': (
            "Популярний маршрут на Боржаві. "
            "Можна піднятися на витягу, далі пішки по хребту."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Shypit_waterfall_2019.jpg/800px-Shypit_waterfall_2019.jpg',
        'coordinates': '48.5891, 23.3012',
    },
    {
        'name': 'Шпиці',
        'region': 'Івано-Франківська обл.',
        'height': 1863,
        'difficulty': 'medium',
        'duration': 7.0,
        'distance': 14.0,
        'description': (
            "Скелі, схожі на вежі готичного замку. "
            "Неймовірно фотогенічне місце в масиві Чорногора."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Spitsi_mountain.jpg/800px-Spitsi_mountain.jpg',
        'coordinates': '48.0986, 24.5441',
    },
    {
        'name': "Хом'як",
        'region': 'Івано-Франківська обл.',
        'height': 1542,
        'difficulty': 'easy',
        'duration': 4.5,
        'distance': 9.0,
        'description': (
            "Ідеальна гора для початківців. "
            "Серпантинна стежка через ліс, на вершині — статуя Матері Божої."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Gorgany_Synyak.jpg/800px-Gorgany_Synyak.jpg',
        'coordinates': '48.3658, 24.5011',
    },
    {
        'name': 'Озеро Несамовите',
        'region': 'Івано-Франківська обл.',
        'height': 1750,
        'difficulty': 'medium',
        'duration': 6.0,
        'distance': 14.0,
        'description': (
            "Одне з найвищих озер України. "
            "Легенда каже: кинь камінь у воду — піде дощ."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Nesamovyte_lake.jpg/800px-Nesamovyte_lake.jpg',
        'coordinates': '48.0701, 24.5639',
    },
    {
        'name': 'Парашка',
        'region': 'Львівська обл.',
        'height': 1268,
        'difficulty': 'medium',
        'duration': 6.0,
        'distance': 13.0,
        'description': (
            "Найвища вершина Сколівських Бескидів. "
            "Гарний варіант для одноденного походу зі Львова."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Parashka_mountain.jpg/800px-Parashka_mountain.jpg',
        'coordinates': '49.0247, 23.4958',
    },
    {
        'name': 'Полонина Руна',
        'region': 'Закарпатська обл.',
        'height': 1479,
        'difficulty': 'easy',
        'duration': 5.0,
        'distance': 12.0,
        'description': (
            "Величезне рівне плато. "
            "Тут збереглися залишки старої радарної станції."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Borzhava_Range.jpg/800px-Borzhava_Range.jpg',
        'coordinates': '48.6712, 23.1084',
    },
    {
        'name': 'Явірник-Горган',
        'region': 'Івано-Франківська обл.',
        'height': 1467,
        'difficulty': 'medium',
        'duration': 5.5,
        'distance': 11.0,
        'description': (
            "Класичні Горгани з каменем, вкритим зеленим мохом. "
            "Дуже атмосферний маршрут."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Yavirnyk-Gorgan.jpg/800px-Yavirnyk-Gorgan.jpg',
        'coordinates': '48.4503, 24.2147',
    },
    {
        'name': 'Пікуй',
        'region': 'Львівська обл.',
        'height': 1408,
        'difficulty': 'medium',
        'duration': 6.5,
        'distance': 12.5,
        'description': (
            "Найвища точка Львівщини. "
            "Гостра вершина з краєвидами на польський бік."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Pikuy_mountain.jpg/800px-Pikuy_mountain.jpg',
        'coordinates': '49.0681, 23.2114',
    },
    {
        'name': 'Бребенескул',
        'region': 'Івано-Франківська обл.',
        'height': 2035,
        'difficulty': 'hard',
        'duration': 8.0,
        'distance': 18.0,
        'description': (
            "Друга за висотою вершина України. "
            "Поруч — найвисокогірніше озеро країни."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Brebeneskul_lake.jpg/800px-Brebeneskul_lake.jpg',
        'coordinates': '48.1042, 24.5391',
    },
    {
        'name': 'Гут-Томнатик',
        'region': 'Івано-Франківська обл.',
        'height': 2016,
        'difficulty': 'hard',
        'duration': 8.5,
        'distance': 19.0,
        'description': (
            "Один із двотисячників Чорногори. "
            "Менш людний за Говерлу, але не менш красивий."
        ),
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Hoverla_View.jpg/800px-Hoverla_View.jpg',
        'coordinates': '48.1203, 24.4897',
    },
]

REVIEW_TEMPLATES = [
    ('Краєвиди просто неймовірні, варто кожного кроку.', 5),
    ('Маршрут важчий, ніж очікував, але воно того варте.', 4),
    ('Дуже багато туристів, тиші не знайти.', 3),
    ('Обов\'язково беріть зручне взуття і достатньо води.', 5),
    ('Найкращий похід у моєму житті.', 5),
    ('Погода зіпсувалась, нічого не побачили.', 2),
    ('Добре маркований маршрут, заблукати важко.', 5),
    ('Рекомендую йти восени — кольори лісу неймовірні.', 5),
    ('Підйом нудний, але вершина компенсує все.', 4),
    ('Дуже крутий спуск, коліна відчутно навантажуються.', 4),
]

REVIEWS_TARGET_COUNT = 40
DEFAULT_PASSWORD = 'password123'


def _fetch_image(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read()
    except Exception as exc:
        print(f'  Не вдалося завантажити {url}: {exc}')
        return None


def _create_users() -> list[User]:
    users = []
    for username, first, last in USERS:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': first,
                'last_name': last,
            },
        )
        if created:
            user.set_password(DEFAULT_PASSWORD)
            user.save()
            print(f'  Створено користувача: {username}')
        users.append(user)
    return users


def _create_routes() -> list[MountainRoute]:
    routes = []
    for data in ROUTES:
        route, created = MountainRoute.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'difficulty': data['difficulty'],
                'height': data['height'],
                'duration_hours': data['duration'],
                'distance_km': data['distance'],
                'region': data['region'],
                'map_coordinates': data['coordinates'],
                'rating': 0,
            },
        )
        if created or not route.image:
            print(f'  Завантажую фото для: {route.name}')
            image_data = _fetch_image(data['image_url'])
            if image_data:
                route.image.save(f'route_{route.pk}.jpg', ContentFile(image_data), save=True)
        else:
            print(f'  Існує: {route.name}')
        routes.append(route)
    return routes


def _create_reviews(users: list[User], routes: list[MountainRoute]) -> int:
    RouteReview.objects.all().delete()
    count = 0
    attempts = 0
    max_attempts = REVIEWS_TARGET_COUNT * 3

    while count < REVIEWS_TARGET_COUNT and attempts < max_attempts:
        attempts += 1
        user = random.choice(users)
        route = random.choice(routes)
        if RouteReview.objects.filter(user=user, route=route).exists():
            continue
        text, base_rating = random.choice(REVIEW_TEMPLATES)
        rating = max(1, min(5, base_rating + random.randint(-1, 1)))
        RouteReview.objects.create(
            user=user,
            route=route,
            rating=rating,
            title=text[:40],
            text=text,
            helpful_count=random.randint(0, 15),
        )
        count += 1

    return count


def populate():
    print('Починаємо наповнення бази даних...')

    with transaction.atomic():
        print('\n[1/3] Користувачі')
        users = _create_users()
        print(f'  Всього: {len(users)}')

        print('\n[2/3] Маршрути')
        routes = _create_routes()
        print(f'  Всього: {len(routes)}')

        print('\n[3/3] Відгуки')
        review_count = _create_reviews(users, routes)
        print(f'  Створено: {review_count}')

    print('\nГотово. Сервер можна запускати.')


if __name__ == '__main__':
    populate()
