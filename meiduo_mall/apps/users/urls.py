from django.urls import path
from apps.users.views import UsernameCount,UserRegister,SendMessageView


urlpatterns = [
    path('usernames/<username:username>/count/', UsernameCount.as_view()),
    path('register/', UserRegister.as_view()),
    path('sms_codes/<mobile>/',SendMessageView.as_view())

]