from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from ..models import MountainRoute, RouteReview, UserProfile


class HomePageView(TemplateView):
    template_name = 'mountains_roads/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_routes'] = MountainRoute.objects.all()[:3]
        context['total_routes'] = MountainRoute.objects.count()
        context['total_reviews'] = RouteReview.objects.count()
        return context


class RoutesListView(ListView):
    model = MountainRoute
    template_name = 'mountains_roads/routes_list.html'
    context_object_name = 'routes'
    paginate_by = 12

    def get_queryset(self):
        queryset = MountainRoute.objects.all()

        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        region = self.request.GET.get('region')
        if region:
            queryset = queryset.filter(region=region)

        min_height = self.request.GET.get('min_height')
        if min_height and min_height.isdigit():
            queryset = queryset.filter(height__gte=int(min_height))

        max_height = self.request.GET.get('max_height')
        if max_height and max_height.isdigit():
            queryset = queryset.filter(height__lte=int(max_height))

        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        allowed_sorts = {
            '-rating', 'rating', 'name', '-name', 'height', '-height',
            'duration_hours', '-duration_hours',
        }
        sort = self.request.GET.get('sort', '-rating')
        if sort not in allowed_sorts:
            sort = '-rating'

        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = MountainRoute.objects.values_list('region', flat=True).distinct()
        context['difficulties'] = MountainRoute.DIFFICULTY_CHOICES
        return context


class RouteDetailView(DetailView):
    model = MountainRoute
    template_name = 'mountains_roads/route_detail.html'
    context_object_name = 'route'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.select_related('user').all()
        context['average_rating'] = self.object.get_average_rating()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_favorite'] = profile.favorite_routes.filter(pk=self.object.pk).exists()
            context['is_completed'] = profile.completed_routes.filter(pk=self.object.pk).exists()

        return context
