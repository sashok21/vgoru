from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AuthorRequiredMixin(UserPassesTestMixin):
    """Дозволяє доступ лише автору об'єкта."""

    author_field = 'user'

    def test_func(self):
        obj = self.get_object()
        return getattr(obj, self.author_field) == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied


class SuccessMessageMixin:
    """Показує повідомлення після успішного виконання форми."""

    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class CssWidgetMixin:
    """Додає CSS-клас form-control до всіх полів форми."""

    widget_class = 'form-control'
    excluded_field_types = ('CheckboxInput', 'RadioSelect', 'CheckboxSelectMultiple')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget_name = field.widget.__class__.__name__
            if widget_name not in self.excluded_field_types:
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing} {self.widget_class}'.strip()
