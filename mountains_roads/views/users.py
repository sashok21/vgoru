from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from ..mixins import SuccessMessageMixin
from ..models import RouteReview, UserProfile
from ..forms import UserRegistrationForm, UserProfileForm


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'mountains_roads/register.html'
    success_url = reverse_lazy('mountains_roads:login')
    success_message = 'Реєстрація успішна! Тепер ви можете увійти.'


class UserProfileView(DetailView):
    model = User
    template_name = 'mountains_roads/user_profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        profile, _ = UserProfile.objects.get_or_create(user=profile_user)
        context['completed_routes'] = profile.completed_routes.all()
        context['favorite_routes'] = profile.favorite_routes.all()
        context['user_reviews'] = RouteReview.objects.filter(user=profile_user).select_related('route')
        context['is_own_profile'] = self.request.user == profile_user
        return context


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'mountains_roads/profile_edit.html'
    success_message = 'Профіль оновлено.'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy(
            'mountains_roads:user-profile',
            kwargs={'username': self.request.user.username},
        )
