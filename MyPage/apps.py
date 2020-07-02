from django.apps import AppConfig


class MypageConfig(AppConfig):
    name = 'MyPage'

    def ready(self):
        import MyPage.signals