"""
Кастомні шаблонні теги для VGoru.

Використання в шаблоні:
    {% load vgoru_tags %}

    {# Активне посилання в навбарі #}
    <a href="..." class="navbar__link {% active_link request 'mountains_roads:home' %}">Головна</a>

    {# Зірковий рейтинг #}
    {% star_rating review.rating %}

    {# Пагінація — URL зі збереженням фільтрів, але з новим page #}
    <a href="{% pagination_url request 3 %}">Сторінка 3</a>
"""
from django import template
from django.urls import reverse, NoReverseMatch
from urllib.parse import urlencode

register = template.Library()


# ---------------------------------------------------------------------------
# {% active_link request url_name [*args] [kwarg=value ...] %}
# ---------------------------------------------------------------------------

@register.simple_tag
def active_link(request, url_name, *args, **kwargs):
    """
    Повертає рядок 'navbar__link--active' якщо поточний шлях збігається
    з URL, побудованим за url_name (та опціональними аргументами).
    Інакше повертає порожній рядок.

    Приклад:
        class="navbar__link {% active_link request 'mountains_roads:home' %}"
    """
    try:
        resolved_url = reverse(url_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return ''
    return 'navbar__link--active' if request.path == resolved_url else ''


# ---------------------------------------------------------------------------
# {% star_rating value %}  →  повертає HTML рядок із зірками
# ---------------------------------------------------------------------------

@register.inclusion_tag('mountains_roads/partials/star_rating.html')
def star_rating(rating):
    """
    Рендерить зірковий рейтинг через partial-шаблон.

    Замість:
        {% with rating=review.rating %}
            {% include 'mountains_roads/partials/star_rating.html' %}
        {% endwith %}
    Тепер достатньо:
        {% star_rating review.rating %}
    """
    return {'rating': rating}


# ---------------------------------------------------------------------------
# {% pagination_url request page_number %}
# ---------------------------------------------------------------------------

@register.simple_tag
def pagination_url(request, page_number):
    """
    Будує URL для пагінації, зберігаючи всі поточні GET-параметри,
    але замінюючи (або додаючи) параметр 'page'.

    Вирішує проблему дублювання 'page' при використанні
    request.GET.urlencode() у циклі пагінатора.

    Приклад:
        <a href="{% pagination_url request page_obj.next_page_number %}">›</a>
    """
    params = request.GET.copy()
    params['page'] = page_number
    return f'?{params.urlencode()}'
