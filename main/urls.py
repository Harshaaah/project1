from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/client', views.register_user, name='register'),
    path('registercounsellor/', views.register_counselor, name='registercounsellor'),
    path('book_counsellor/', views.book_counsellor, name='book_counsellor'),
    path('client_dashboard/',views.client_dashboard, name='client_dashboard'),
    path('counsellor_dashboard/',views.client_dashboard, name='counsellor_dashboard'),
    path('logout/',views.logout_view, name='logout'),
]


