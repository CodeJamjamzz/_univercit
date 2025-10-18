from django.urls import path
from views import LoginView, HomeView

urlpatterns = [
    path('login/', LoginView),
    path('', HomeView)
]
