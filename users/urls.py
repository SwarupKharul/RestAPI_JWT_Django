from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, Profile

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('profile/', Profile.as_view(), name="profile"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
