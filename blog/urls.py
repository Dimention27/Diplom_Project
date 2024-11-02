from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('contacts/', views.contacts, name='blog-contacts'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name="register"),
]
