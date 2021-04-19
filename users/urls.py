from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, Profile, ProfileList

app_name = 'users'

urlpatterns = [
    path('', ProfileList.as_view(), name="profilelist"),
    path('<int:pk>/', Profile.as_view(), name="profile"),
]
