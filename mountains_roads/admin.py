from django.contrib import admin
from django.utils.html import format_html

from .models import MountainRoute, RouteReview, UserProfile


class RouteReviewInline(admin.TabularInline):
    model = RouteReview
    extra = 0
    fields = ('user', 'rating', 'title', 'text', 'helpful_count', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(MountainRoute)
class MountainRouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'difficulty', 'height', 'rating_display', 'reviews_count', 'created_at')
    list_display_links = ('name',)
    list_filter = ('difficulty', 'region')
    search_fields = ('name', 'description', 'region')
    ordering = ('-rating', '-created_at')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at', 'rating')
    inlines = [RouteReviewInline]
    actions = ['recalculate_ratings']

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'description', 'region', 'difficulty'),
        }),
        ('Параметри маршруту', {
            'fields': ('height', 'duration_hours', 'distance_km'),
        }),
        ('Медіа та навігація', {
            'fields': ('image', 'gpx_file', 'map_coordinates'),
        }),
        ('Статистика', {
            'fields': ('rating', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Рейтинг', ordering='rating')
    def rating_display(self, obj):
        if obj.rating == 0:
            return '—'
        filled = round(obj.rating)
        stars = '★' * filled + '☆' * (5 - filled)
        rating_str = '{:.1f}'.format(obj.rating)
        return format_html('<span title="{}">{} {}</span>', rating_str, stars, rating_str)

    @admin.display(description='Відгуків')
    def reviews_count(self, obj):
        count = obj.reviews.count()
        if count == 0:
            return '0'
        url = f'/admin/mountains_roads/routereview/?route__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)

    @admin.action(description='Перерахувати рейтинги вибраних маршрутів')
    def recalculate_ratings(self, request, queryset):
        updated = 0
        for route in queryset:
            route.refresh_rating()
            updated += 1
        self.message_user(request, f'Рейтинги перераховано для {updated} маршрут(ів).')


@admin.register(RouteReview)
class RouteReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'rating', 'title', 'created_at')
    list_display_links = ('title',)
    list_filter = ('rating',)
    search_fields = ('title', 'text', 'user__username', 'route__name')
    ordering = ('-created_at',)
    list_per_page = 25
    list_select_related = ('user', 'route')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed_count', 'favorites_count', 'created_at')
    list_display_links = ('user',)
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('completed_routes', 'favorite_routes')
    ordering = ('-created_at',)
    list_select_related = ('user',)

    @admin.display(description='Пройдено маршрутів')
    def completed_count(self, obj):
        return obj.completed_routes.count()

    @admin.display(description='Улюблених маршрутів')
    def favorites_count(self, obj):
        return obj.favorite_routes.count()