from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('contacts/', views.contacts, name='blog-contacts'),
    # path('sign_up/', views.registration, name='blog-registration'),
    path('add_post/', views.add_post, name='add_post'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name="register"),
]
