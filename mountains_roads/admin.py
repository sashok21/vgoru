from django.contrib import admin

from .models import MountainRoute, RouteReview, UserProfile


@admin.register(MountainRoute)
class MountainRouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'difficulty', 'height', 'rating', 'created_at')
    list_display_links = ('name',)
    list_filter = ('difficulty', 'region')
    search_fields = ('name', 'description', 'region')
    ordering = ('-rating', '-created_at')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at', 'rating')

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
