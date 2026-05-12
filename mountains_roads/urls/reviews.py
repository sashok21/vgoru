from django.urls import path

from ..views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('routes/<int:route_id>/review/add/', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
