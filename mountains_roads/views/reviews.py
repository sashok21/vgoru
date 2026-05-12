from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from ..mixins import AuthorRequiredMixin, SuccessMessageMixin
from ..models import MountainRoute, RouteReview
from ..forms import RouteReviewForm


class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RouteReview
    form_class = RouteReviewForm
    template_name = 'mountains_roads/review_form.html'
    success_message = 'Дякуємо за відгук!'

    def dispatch(self, request, *args, **kwargs):
        self.route = get_object_or_404(MountainRoute, pk=kwargs['route_id'])
        if request.user.is_authenticated:
            if RouteReview.objects.filter(route=self.route, user=request.user).exists():
                messages.error(request, 'Ви вже залишили відгук до цього маршруту.')
                return redirect('mountains_roads:route-detail', pk=self.route.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.route = self.route
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mountains_roads:route-detail', kwargs={'pk': self.route.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['route'] = self.route
        return context


class ReviewUpdateView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RouteReview
    form_class = RouteReviewForm
    template_name = 'mountains_roads/review_form.html'
    success_message = 'Відгук оновлено.'

    def get_success_url(self):
        return reverse_lazy('mountains_roads:route-detail', kwargs={'pk': self.object.route.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['route'] = self.object.route
        return context


class ReviewDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = RouteReview
    template_name = 'mountains_roads/review_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('mountains_roads:route-detail', kwargs={'pk': self.object.route.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Відгук видалено.')
        return super().form_valid(form)
