from django.urls import path
from accounts import views
app_name = 'accounts'
urlpatterns = [
    #registration
    path('signup/',views.signup_view,name='signup'),
    #log in
    path('login/',views.login_view,name='login'),
    #log out
    path('logout/',views.logout_view,name='logout'),
    #profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit-profile'),
]