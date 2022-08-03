from django.urls import path
from apps.users.views import UsernameCount,UserRegister


urlpatterns = [
    path('usernames/<username:username>/count/', UsernameCount.as_view()),
    path('register/', UserRegister.as_view()),

]