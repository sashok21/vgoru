from django.urls import path, include

app_name = 'mountains_roads'

urlpatterns = [
    path('', include('mountains_roads.urls.routes')),
    path('', include('mountains_roads.urls.reviews')),
    path('', include('mountains_roads.urls.users')),
]
