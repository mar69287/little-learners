from django.apps import AppConfig


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

def ready(self):
    import main_app.models
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    permission = Permission.objects.get(codename='is_teacher')
    teacher_group.permissions.add(permission)
