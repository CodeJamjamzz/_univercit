from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', SignInView.as_view(), name="signin"),
    path('login/', LogInView.as_view(), name="login"),
    path('', HomeView.as_view(), name="index")
]
