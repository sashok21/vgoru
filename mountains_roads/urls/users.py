from django.urls import path
from django.contrib.auth import views as auth_views

from ..views import UserRegistrationView, UserProfileView, UserProfileUpdateView
from ..views import toggle_favorite, toggle_completed

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='mountains_roads/login.html',
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mountains_roads:home'), name='logout'),
    # edit стоїть ПЕРЕД <username>, щоб не перекривався
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('routes/<int:route_id>/toggle-favorite/', toggle_favorite, name='toggle-favorite'),
    path('routes/<int:route_id>/toggle-completed/', toggle_completed, name='toggle-completed'),
]
