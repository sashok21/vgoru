from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag
def active_link(request, url_name, *args, **kwargs):
    try:
        resolved_url = reverse(url_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return ''
    return 'navbar__link--active' if request.path == resolved_url else ''


@register.inclusion_tag('mountains_roads/partials/star_rating.html')
def star_rating(rating):
    return {'rating': rating}


@register.simple_tag
def pagination_url(request, page_number):
    params = request.GET.copy()
    params['page'] = page_number
    return f'?{params.urlencode()}'