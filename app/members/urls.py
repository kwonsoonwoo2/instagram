from django.urls import path

from members import views

app_name = 'members'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('facebook-login/', views.facebook_login, name='facebook-login')
]