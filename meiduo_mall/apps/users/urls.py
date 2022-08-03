from django.urls import path
from apps.users.views import UsernameCount
urlpatterns = [
    path('usernames/<username>/count/', UsernameCount.as_view()),
]