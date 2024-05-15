from django.urls import path, include
from . import views


app_name = "messenger"

urlpatterns=[
    path('', views.messenger, name='messenger'),
    path('<int:user_id>', views.thread, name="thread"),
]