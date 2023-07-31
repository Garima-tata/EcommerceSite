from django.urls import path
from SiteAuth import views
urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activateView.as_view(), name='activate'),
    path('request-rest-email/', views.RequestRestEmail.as_view(), name='request-rest-email'),
    path('set-new-password/<uidb64>/<token>/', views.SetNewPasswordView.as_view(), name='set-new-password'),
    
]