from django.urls import path

from ..views import HomePageView, RoutesListView, RouteDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('routes/', RoutesListView.as_view(), name='routes-list'),
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='route-detail'),
]
