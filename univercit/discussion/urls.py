from django.urls import path
from . import views

urlpatterns = [
    path('forum/<int:forum_id>', views.forum_view, name='forum'),
    path('thread/<int:thread_id>', views.thread_view, name='thread'),
    path('forum/<int:forum_id>/threads', views.add_thread, name='add_thread'),
    path('thread/<int:thread_id>/comments', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply', views.add_reply, name='add_reply')
]