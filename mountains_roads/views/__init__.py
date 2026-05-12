from .routes import HomePageView, RoutesListView, RouteDetailView
from .reviews import ReviewCreateView, ReviewUpdateView, ReviewDeleteView
from .users import UserRegistrationView, UserProfileView, UserProfileUpdateView
from .ajax import toggle_favorite, toggle_completed

__all__ = [
    'HomePageView',
    'RoutesListView',
    'RouteDetailView',
    'ReviewCreateView',
    'ReviewUpdateView',
    'ReviewDeleteView',
    'UserRegistrationView',
    'UserProfileView',
    'UserProfileUpdateView',
    'toggle_favorite',
    'toggle_completed',
]
