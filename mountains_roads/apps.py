from django.apps import AppConfig


class MountainsRoadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mountains_roads'
    verbose_name = 'Гірські маршрути'

    def ready(self):
        import mountains_roads.signals  # noqa: F401
