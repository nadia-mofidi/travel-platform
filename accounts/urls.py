from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    #registration
    path('signup/',views.signup_view,name='signup'),
    #log in
    path('login/',views.login_view,name='login'),
    #log out
    path('logout/',views.logout_view,name='logout'),
    
]