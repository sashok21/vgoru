from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

from ..models import MountainRoute


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


@login_required
def toggle_favorite(request, route_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    route = get_object_or_404(MountainRoute, pk=route_id)
    profile = request.user.profile

    if profile.favorite_routes.filter(pk=route.pk).exists():
        profile.favorite_routes.remove(route)
        is_favorite = False
        message = 'Маршрут видалено з улюблених.'
    else:
        profile.favorite_routes.add(route)
        is_favorite = True
        message = 'Маршрут додано до улюблених.'

    if _is_ajax(request):
        return JsonResponse({'is_favorite': is_favorite, 'message': message})

    messages.success(request, message)
    return redirect('mountains_roads:route-detail', pk=route_id)


@login_required
def toggle_completed(request, route_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    route = get_object_or_404(MountainRoute, pk=route_id)
    profile = request.user.profile

    if profile.completed_routes.filter(pk=route.pk).exists():
        profile.completed_routes.remove(route)
        is_completed = False
        message = 'Маршрут позначено як не пройдено.'
    else:
        profile.completed_routes.add(route)
        is_completed = True
        message = 'Маршрут позначено як пройдено.'

    if _is_ajax(request):
        return JsonResponse({'is_completed': is_completed, 'message': message})

    messages.success(request, message)
    return redirect('mountains_roads:route-detail', pk=route_id)
