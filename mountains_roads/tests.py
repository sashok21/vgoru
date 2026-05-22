from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from .models import MountainRoute, RouteReview, UserProfile
from .forms import UserRegistrationForm
from .views import UserProfileUpdateView, UserProfileView


def make_route(**kwargs) -> MountainRoute:
    defaults = dict(
        name='Говерла',
        description='Найвища точка України.',
        difficulty=MountainRoute.DIFFICULTY_MEDIUM,
        height=2061,
        duration_hours=6.0,
        distance_km=14.5,
        region='Івано-Франківська обл.',
        map_coordinates='48.1614, 24.5003',
    )
    defaults.update(kwargs)
    return MountainRoute.objects.create(**defaults)


def make_user(username='testuser', password='testpass123') -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        email=f'{username}@example.com',
    )


class MountainRouteModelTest(TestCase):

    def setUp(self):
        self.route = make_route()
        self.user1 = make_user('user1')
        self.user2 = make_user('user2')

    def test_get_absolute_url_resolves(self):
        url = self.route.get_absolute_url()
        self.assertEqual(url, f'/routes/{self.route.pk}/')

    def test_get_absolute_url_is_accessible(self):
        response = self.client.get(self.route.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_average_rating_no_reviews(self):
        self.assertEqual(self.route.get_average_rating(), 0)

    def test_average_rating_single_review(self):
        RouteReview.objects.create(
            route=self.route, user=self.user1,
            rating=4, title='Добре', text='Текст',
        )
        self.assertEqual(self.route.get_average_rating(), 4.0)

    def test_average_rating_multiple_reviews(self):
        RouteReview.objects.create(
            route=self.route, user=self.user1,
            rating=5, title='Чудово', text='Текст',
        )
        RouteReview.objects.create(
            route=self.route, user=self.user2,
            rating=3, title='Середньо', text='Текст',
        )
        self.assertAlmostEqual(self.route.get_average_rating(), 4.0)

    def test_refresh_rating_updates_db_field(self):
        RouteReview.objects.create(
            route=self.route, user=self.user1,
            rating=5, title='Топ', text='Текст',
        )
        RouteReview.objects.create(
            route=self.route, user=self.user2,
            rating=3, title='Нічого', text='Текст',
        )
        self.route.refresh_rating()
        self.route.refresh_from_db()
        self.assertAlmostEqual(self.route.rating, 4.0)

    def test_refresh_rating_zero_when_no_reviews(self):
        self.route.rating = 4.5
        self.route.save(update_fields=['rating'])
        self.route.refresh_rating()
        self.route.refresh_from_db()
        self.assertEqual(self.route.rating, 0)

    def test_str(self):
        self.assertEqual(str(self.route), 'Говерла')


class SignalsTest(TestCase):

    def test_user_profile_created_on_user_save(self):
        user = make_user('signaluser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_only_one_profile_per_user(self):
        user = make_user('onlyone')
        user.save()
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

    def test_rating_updates_on_review_create(self):
        route = make_route(name='Петрос')
        user = make_user('ratinguser')
        RouteReview.objects.create(
            route=route, user=user,
            rating=5, title='Топ', text='Текст',
        )
        route.refresh_from_db()
        self.assertAlmostEqual(route.rating, 5.0)

    def test_rating_updates_on_review_delete(self):
        route = make_route(name='Синевир')
        user1 = make_user('del1')
        user2 = make_user('del2')
        review1 = RouteReview.objects.create(
            route=route, user=user1,
            rating=5, title='Топ', text='Текст',
        )
        RouteReview.objects.create(
            route=route, user=user2,
            rating=3, title='Ок', text='Текст',
        )
        route.refresh_from_db()
        self.assertAlmostEqual(route.rating, 4.0)

        review1.delete()
        route.refresh_from_db()
        self.assertAlmostEqual(route.rating, 3.0)


class ViewStatusCodeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.route = make_route()
        self.user = make_user()

    def test_home_page_ok(self):
        response = self.client.get(reverse('mountains_roads:home'))
        self.assertEqual(response.status_code, 200)

    def test_routes_list_ok(self):
        response = self.client.get(reverse('mountains_roads:routes-list'))
        self.assertEqual(response.status_code, 200)

    def test_route_detail_ok(self):
        response = self.client.get(
            reverse('mountains_roads:route-detail', kwargs={'pk': self.route.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_route_detail_404_on_missing(self):
        response = self.client.get(
            reverse('mountains_roads:route-detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_login_page_ok(self):
        response = self.client.get(reverse('mountains_roads:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_ok(self):
        response = self.client.get(reverse('mountains_roads:register'))
        self.assertEqual(response.status_code, 200)

    def test_review_create_redirects_anonymous(self):
        response = self.client.get(
            reverse('mountains_roads:review-create', kwargs={'route_id': self.route.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_profile_edit_redirects_anonymous(self):
        response = self.client.get(reverse('mountains_roads:profile-edit'))
        self.assertEqual(response.status_code, 302)

    def test_toggle_favorite_redirects_anonymous(self):
        response = self.client.post(
            reverse('mountains_roads:toggle-favorite', kwargs={'route_id': self.route.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_review_create_ok_when_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('mountains_roads:review-create', kwargs={'route_id': self.route.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_view_ok(self):
        response = self.client.get(
            reverse('mountains_roads:user-profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_routes_list_filter_by_difficulty(self):
        make_route(name='Легкий', difficulty=MountainRoute.DIFFICULTY_EASY)
        response = self.client.get(
            reverse('mountains_roads:routes-list') + '?difficulty=easy'
        )
        self.assertEqual(response.status_code, 200)
        for route in response.context['routes']:
            self.assertEqual(route.difficulty, MountainRoute.DIFFICULTY_EASY)

    def test_routes_list_search(self):
        make_route(name='Унікальна Назва XYZ')
        response = self.client.get(
            reverse('mountains_roads:routes-list') + '?search=Унікальна+Назва+XYZ'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Унікальна Назва XYZ')


class UserRegistrationFormTest(TestCase):

    BASE_DATA = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password1': 'StrongPass99!',
        'password2': 'StrongPass99!',
    }

    def test_valid_form(self):
        form = UserRegistrationForm(data=self.BASE_DATA)
        self.assertTrue(form.is_valid(), form.errors)

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            username='existing', email='new@example.com', password='pass'
        )
        form = UserRegistrationForm(data=self.BASE_DATA)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch_rejected(self):
        data = {**self.BASE_DATA, 'password2': 'WrongPass99!'}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_missing_email_rejected(self):
        data = {**self.BASE_DATA, 'email': ''}
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class UrlResolutionTest(TestCase):

    def test_profile_edit_resolves_to_update_view(self):
        resolved = resolve('/profile/edit/')
        self.assertEqual(resolved.func.view_class, UserProfileUpdateView)

    def test_profile_username_resolves_to_detail_view(self):
        resolved = resolve('/profile/someuser/')
        self.assertEqual(resolved.func.view_class, UserProfileView)

    def test_edit_does_not_resolve_to_profile_view(self):
        resolved = resolve('/profile/edit/')
        self.assertNotEqual(resolved.func.view_class, UserProfileView)


class AjaxToggleTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.route = make_route()
        self.client.login(username='testuser', password='testpass123')

    def _ajax_post(self, url):
        return self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_toggle_favorite_adds(self):
        response = self._ajax_post(
            reverse('mountains_roads:toggle-favorite', kwargs={'route_id': self.route.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_favorite'])

    def test_toggle_favorite_removes(self):
        self.user.profile.favorite_routes.add(self.route)
        response = self._ajax_post(
            reverse('mountains_roads:toggle-favorite', kwargs={'route_id': self.route.pk})
        )
        self.assertFalse(response.json()['is_favorite'])

    def test_toggle_completed_adds(self):
        response = self._ajax_post(
            reverse('mountains_roads:toggle-completed', kwargs={'route_id': self.route.pk})
        )
        self.assertTrue(response.json()['is_completed'])

    def test_toggle_favorite_get_returns_405(self):
        response = self.client.get(
            reverse('mountains_roads:toggle-favorite', kwargs={'route_id': self.route.pk})
        )
        self.assertEqual(response.status_code, 405)