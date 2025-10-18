from django.urls import path
from . import views

urlpatterns = [
    path('forum/<int:forum_id>', views.forum_view),
    path('thread/<int:thread_id>', views.thread_view)
]